import unittest
import json
from app import app  # Adjust the import based on your file structure

class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        # Create a test client
        self.app = app.test_client()
        self.app.testing = True  # Enable testing mode

    def test_register_endpoint(self):
        # Send a POST request to the endpoint
        data = {
            "password": "password123",
            "email": "testuser@example.com",
            "firstname": "Test",
            "surname": "User",
        }
         
        response = self.app.post('/api/register', 
                                 data=json.dumps(data), 
                                 content_type='application/json')
        # Check the response status code
        print(response.status_code)
    
    def test_login_success(self):
        """Test successful login."""
        response = self.app.post('/api/auth/login', 
                                  data=json.dumps({'email': 'testuser@example.com', 'password': 'password123'}),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.get_json())
    
    def test_login_failure_bad_username(self):
        """Test login failure with a bad username."""
        response = self.app.post('/api/auth/login', 
                                  data=json.dumps({'username': 'wronguser', 'password': 'testpassword'}),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.get_json(), {"msg": "Bad username or password"})

    def test_login_get_user(self):
        email = 'testuser@example.com'
        # Step 1: Log in to get the access token
        login_response = self.app.post('/api/auth/login', 
                                        data=json.dumps({'email': email, 'password': 'password123'}), 
                                        content_type='application/json')
        
        # Check login response and retrieve the token
        self.assertEqual(login_response.status_code, 200)
        token = login_response.json.get('access_token')
        userid = int(login_response.json.get('userid'))
        self.assertIsNotNone(token, "Access token should not be None")

        # Step 2: Use the token to get user information
        user_response = self.app.get(f'/api/user/{userid}',
                                      headers={'Authorization': f'Bearer {token}'})
        
        # Check the response status code for user retrieval
        self.assertEqual(user_response.status_code, 200)

    def test_create_ad(self):
        """Test creating a new ad."""
        
        # Sample data to create a new ad
        data = {
            "created_by": 1,  # Replace with an actual user ID from your database or mock setup
            "title": "Test Project",
            "description": "This is a test project description.",
            "image": "test_image.png",
            "skills_required": "Python, Flask, SQL",
            "project_type": "Open Source",
            "team_size": 3,
            "looking_for_mentor": True,
            "completed": False
        }
        
        # Send a POST request to the create_ad endpoint
        response = self.app.post('/ads',
                                 data=json.dumps(data),
                                 content_type='application/json')
        
        # Check the response status code
        self.assertEqual(response.status_code, 201)
        
        # Check the response data
        response_data = response.get_json()
        self.assertIn("message", response_data)
        self.assertEqual(response_data["message"], "Ad created successfully")
        self.assertIn("projectid", response_data)
        self.assertIsInstance(response_data["projectid"], int)


if __name__ == '__main__':
    unittest.main()