import json
import requests
from flask import request, _request_ctx_stack, abort, jsonify
from functools import wraps
from jose import jwt
from urllib.request import urlopen

AUTH0_DOMAIN = 'fsdn123.au.auth0.com'

ALGORITHMS = ['RS256']
API_AUDIENCE = 'cap2'

JWKS_URL = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
SECRET_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im1BWW5fdF80X0NXOXkzM09sWFlpOSJ9.eyJpc3MiOiJodHRwczovL2ZzZG4xMjMuYXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDY1MjQzY2ZhZTUwMTY0NDM1NGMyN2UyMyIsImF1ZCI6ImNhcDIiLCJpYXQiOjE2OTY5NTc4OTUsImV4cCI6MTY5NzA0NDI5NCwiYXpwIjoidzlXY1ptVkx4OHZuQTZDblc5cHRRNmxhUGk5NW01MVUiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImdldDphY3RvcnMiLCJnZXQ6aG9tZSIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvciIsInBvc3Q6YWN0b3IiXX0.UDgeKuFudkbjO1xTIotMoleNhwEUWu7txvK5n1vbpBzwyfhE1YMPjZHio1I9i2AZNpxtgYY6dUZjQcL99B16GmcHKy2NeLAontpU_c9wrb4OpcvK075WjyB-7LxoK1V95zcrMy6FD_gU4Ibx1goieP48vnTlWhKaMJI97_cGkBnthvw14zunmFEolYT3r4FsUSZOJYm2_SmPQNGDcsjBn21DqEDEzkEDfkBDr6Hq2nf5lsGnjswYtFpy9uhaialO_ac2sQ70LHyJrZ5iUc7f21j4fUO1pDTykAy3uY1f67Wls6vWA1AHb_AOC3dgpRBya7I8tYANZ65tkyBc2OZJVA"

headers = {
        'Authorization': f'Bearer {SECRET_TOKEN}'
    }

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header

'''
@TODO implement get_token_auth_header() method
    it should attempt to get the header from the request
        it should raise an AuthError if no header is present
    it should attempt to split bearer and the token
        it should raise an AuthError if the header is malformed
    return the token part of the header
'''
def get_token_auth_header():
   
   if 'Authorization' not in request.headers:
       print('************Authorization not in request headers******************')
       abort(401)
   auth_header = request.headers['Authorization']
   print(auth_header, '******************************')
   header_parts = auth_header.split(' ')
   if len(header_parts) !=2:
       abort(401)
   elif header_parts[0].lower() !='bearer':
       abort(401)
   return header_parts[1]

'''
@TODO implement check_permissions(permission, payload) method
    @INPUTS
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload

    it should raise an AuthError if permissions are not included in the payload
        !!NOTE check your RBAC settings in Auth0
    it should raise an AuthError if the requested permission string is not in the payload permissions array
    return true otherwise
'''
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


'''
@TODO implement verify_decode_jwt(token) method
    @INPUTS
        token: a json web token (string)

    it should be an Auth0 token with key id (kid)
    it should verify the token using Auth0 /.well-known/jwks.json
    it should decode the payload from the token
    it should validate the claims
    return the decoded payload

    !!NOTE urlopen has a common certificate error described here: https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''
# def get_jwks_data():
    # with urlopen(JWKS_URL) as response:
    #     jwks_data = json.loads(response.read().decode("utf-8"))
    # return jwks_data
def get_jwks_data(JWKS_URL):
    try:
        response = requests.get(JWKS_URL, headers=headers)
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