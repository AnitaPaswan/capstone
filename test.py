import unittest
import requests
import json

class TestActorAPI(unittest.TestCase):
    base_url = 'https://render-capstone-example-5cq7.onrender.com//actors' 

    def test_post_actor(self):
        actor_data = {
            "name": "John Doe",
            "age": "35",
            "gender": "Male",
            "movie_id": 1
        }
        response = requests.post(self.base_url, json=actor_data)
        self.assertEqual(response.status_code, 201)  

    def test_get_actors(self):
        response = requests.get(self.base_url)
        self.assertEqual(response.status_code, 200) 
        actors = response.json()
        self.assertIsInstance(actors, list)

    def test_edit_actor(self):
        actor_data = {
            "name": "Updated Name",
            "age": "40",
            "gender": "Male",
            "movie_id": 1
        }
        response = requests.put(f'{self.base_url}/1', json=actor_data) 
        self.assertEqual(response.status_code, 200)  

    def test_delete_actor(self):
        response = requests.delete(f'{self.base_url}/1') 
        self.assertEqual(response.status_code, 204)  

    def test_bad_request_missing_data(self):
       
        incomplete_data = {
            "name": "John Doe",
            "age": "35"
            # Missing the "gender" and "movie_id" field, which is required
        }
        response = requests.post(self.base_url, json=incomplete_data)
        self.assertEqual(response.status_code, 400)  

    def test_bad_request_invalid_data(self):
        invalid_data = {
            "name": "John Doe",
            "age": "33",  
            "gender": "Male",
            "movie_id": "Thirty-Five", 
        }
        response = requests.post(self.base_url, json=invalid_data)
        self.assertEqual(response.status_code, 400)  



if __name__ == '__main__':
    unittest.main()
