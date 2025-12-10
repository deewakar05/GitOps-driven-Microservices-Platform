"""
Simple test file for the microservice
"""

import unittest
import json
from app import app

class MicroserviceTestCase(unittest.TestCase):
    """Test cases for the microservice API"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app.test_client()
        self.app.testing = True
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
    
    def test_get_users(self):
        """Test getting all users"""
        response = self.app.get('/api/users')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('users', data)
        self.assertIn('count', data)
    
    def test_get_user(self):
        """Test getting a specific user"""
        response = self.app.get('/api/users/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['id'], 1)
    
    def test_get_nonexistent_user(self):
        """Test getting a user that doesn't exist"""
        response = self.app.get('/api/users/999')
        self.assertEqual(response.status_code, 404)
    
    def test_create_user(self):
        """Test creating a new user"""
        new_user = {
            "name": "Test User",
            "email": "test@example.com"
        }
        response = self.app.post(
            '/api/users',
            data=json.dumps(new_user),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Test User')
        self.assertEqual(data['email'], 'test@example.com')
    
    def test_create_user_invalid_data(self):
        """Test creating a user with invalid data"""
        response = self.app.post(
            '/api/users',
            data=json.dumps({"name": "Test"}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
    
    def test_update_user(self):
        """Test updating a user"""
        update_data = {"name": "Updated Name"}
        response = self.app.put(
            '/api/users/1',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Updated Name')
    
    def test_index(self):
        """Test root endpoint"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('message', data)
        self.assertIn('endpoints', data)

if __name__ == '__main__':
    unittest.main()

