"""
Unit tests for User Service
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "user-service"

def test_readiness_check():
    """Test readiness check endpoint"""
    response = client.get("/health/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"

def test_liveness_check():
    """Test liveness check endpoint"""
    response = client.get("/health/live")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "alive"

def test_metrics():
    """Test metrics endpoint"""
    response = client.get("/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "total_users" in data

def test_create_user():
    """Test user creation"""
    user_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "age": 30
    }
    response = client.post("/api/v1/users", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == user_data["name"]
    assert data["email"] == user_data["email"]
    assert data["age"] == user_data["age"]
    assert "id" in data
    assert "created_at" in data

def test_create_duplicate_user():
    """Test creating duplicate user (same email)"""
    user_data = {
        "name": "Jane Doe",
        "email": "jane.doe@example.com",
        "age": 25
    }
    # Create first user
    response1 = client.post("/api/v1/users", json=user_data)
    assert response1.status_code == 201
    
    # Try to create duplicate
    response2 = client.post("/api/v1/users", json=user_data)
    assert response2.status_code == 409

def test_get_user():
    """Test getting user by ID"""
    # Create a user
    user_data = {
        "name": "Test User",
        "email": "test@example.com"
    }
    create_response = client.post("/api/v1/users", json=user_data)
    assert create_response.status_code == 201
    user_id = create_response.json()["id"]
    
    # Get the user
    response = client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["name"] == user_data["name"]

def test_get_nonexistent_user():
    """Test getting non-existent user"""
    response = client.get("/api/v1/users/nonexistent-id")
    assert response.status_code == 404

def test_list_users():
    """Test listing users"""
    # Create a few users
    for i in range(3):
        user_data = {
            "name": f"User {i}",
            "email": f"user{i}@example.com"
        }
        client.post("/api/v1/users", json=user_data)
    
    # List users
    response = client.get("/api/v1/users")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3

def test_update_user():
    """Test updating user"""
    # Create a user
    user_data = {
        "name": "Original Name",
        "email": "original@example.com"
    }
    create_response = client.post("/api/v1/users", json=user_data)
    user_id = create_response.json()["id"]
    
    # Update the user
    update_data = {
        "name": "Updated Name",
        "age": 35
    }
    response = client.put(f"/api/v1/users/{user_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"
    assert data["age"] == 35

def test_delete_user():
    """Test deleting user"""
    # Create a user
    user_data = {
        "name": "To Delete",
        "email": "delete@example.com"
    }
    create_response = client.post("/api/v1/users", json=user_data)
    user_id = create_response.json()["id"]
    
    # Delete the user
    response = client.delete(f"/api/v1/users/{user_id}")
    assert response.status_code == 204
    
    # Verify user is deleted
    get_response = client.get(f"/api/v1/users/{user_id}")
    assert get_response.status_code == 404
