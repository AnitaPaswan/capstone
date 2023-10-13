import json
import requests
from flask import request, _request_ctx_stack, abort, jsonify
from functools import wraps
from jose import jwt
from urllib.request import urlopen
import os

AUTH0_DOMAIN = os.environ['AUTH0_DOMAIN']
API_AUDIENCE = os.environ['API_AUDIENCE']

ALGORITHMS = ['RS256']
#API_AUDIENCE = 'cap2'
#AUTH0_DOMAIN = 'fsdn123.au.auth0.com'

JWKS_URL = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header(): 
   if 'Authorization' not in request.headers:
       return jsonify({'message': 'Authorization token is missing'}), 401
   auth_header = request.headers['Authorization']
   print(auth_header, '*************auth_header*****************')
   header_parts = auth_header.split(' ')
   if len(header_parts) !=2:
       abort(401)
   elif header_parts[0].lower() !='bearer':
       abort(401)
   return header_parts[1]

def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
            }, 400)
    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found..'
            }, 403)
    return True

def get_jwks_data(JWKS_URL):
    try:
        response = requests.get(JWKS_URL)
        response.raise_for_status()  # Raise an exception for HTTP errors
        jwks_data = response.json()
        print('jwks_data',jwks_data)
        return jwks_data
    except requests.exceptions.RequestException as e:
        print("Error fetching JWKS data:", e)
        return None

def get_rsa_key(key_id):
    # Fetch JWKS data from JWKS endpoint
    jwks_response = requests.get(JWKS_URL)
    jwks_data = jwks_response.json()

    # Find the RSA key in JWKS based on 'kid'
    rsa_key = None
    for key in jwks_data['keys']:
        if key['kid'] == key_id:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
            break
    return rsa_key


def verify_decode_jwt(token):
    jwks_data = get_jwks_data(JWKS_URL)
    print(jwks_data)
    unverified_header = jwt.get_unverified_header(token)
    print('unverified_header', unverified_header)
    rsa_key = None
    if 'kid' not in unverified_header:
        
        raise AuthError({
            'code' : 'Invalid header',
            'description' : 'Authorization malformed'
        }, 401)
    
    for key in jwks_data['keys']:
        if key['kid']== unverified_header['kid']:
            rsa_key = {
                'kty' : key['kty'],
                'kid' : key['kid'],
                'use' : key['use'],
                'n': key['n'],
                'e': key['e']
            }
            break
        print(rsa_key)
        return rsa_key
    
def requires_auth(permission):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            print(token,' ****************token********************')
            if not token:
                return jsonify({'message': 'Authorization token is missing'}), 401
            try:
                unverified_header = jwt.get_unverified_header(token)
                print(unverified_header, 'klsjkjsdgi')
                rsa_key = get_rsa_key(unverified_header['kid'])
                #rsa_key = verify_decode_jwt(token)

                if rsa_key:
                    decoded_payload = jwt.decode(token, rsa_key, algorithms=ALGORITHMS, audience=API_AUDIENCE, issuer='https://'+ AUTH0_DOMAIN +'/')
                    print(decoded_payload)
                    permissions = check_permissions(permission, decoded_payload)
                    
                    if permissions:  # If permission is specified, check authorization
                        if 'permissions' in decoded_payload and permission in decoded_payload['permissions']:
                            return f(decoded_payload, *args, **kwargs)
                        else:
                            raise AuthError({
                               'code': 'Forbidden',
                               'description': 'Permission denied'}, 403)

                    else:
                        return f(decoded_payload, *args, **kwargs)
                else:
                     raise AuthError({
                         'code': 'RSA key not found',
                         'description': 'RSA key not found in JWKS'}, 401) 

            except jwt.ExpiredSignatureError:
                raise AuthError({
                    'code': 'token_expired',
                    'description': 'Token Expired'}, 401)
        return wrapper
    return decorator