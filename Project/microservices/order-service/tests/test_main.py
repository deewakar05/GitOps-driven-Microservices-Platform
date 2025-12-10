"""
Unit tests for Order Service
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from app.main import app

client = TestClient(app)

@pytest.fixture
def mock_user_service():
    """Mock user service responses"""
    with patch("app.main.verify_user_exists") as mock:
        mock.return_value = True
        yield mock

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "order-service"

def test_readiness_check():
    """Test readiness check endpoint"""
    response = client.get("/health/ready")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "dependencies" in data

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
    assert "total_orders" in data

def test_create_order(mock_user_service):
    """Test order creation"""
    order_data = {
        "user_id": "test-user-123",
        "items": [
            {
                "product_id": "prod-1",
                "product_name": "Test Product",
                "quantity": 2,
                "price": 10.99
            }
        ],
        "shipping_address": "123 Test St, Test City"
    }
    response = client.post("/api/v1/orders", json=order_data)
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == order_data["user_id"]
    assert data["status"] == "pending"
    assert data["total_amount"] == 21.98  # 2 * 10.99
    assert "id" in data
    assert "created_at" in data

def test_create_order_invalid_user(mock_user_service):
    """Test creating order with non-existent user"""
    mock_user_service.return_value = False
    order_data = {
        "user_id": "non-existent-user",
        "items": [
            {
                "product_id": "prod-1",
                "product_name": "Test Product",
                "quantity": 1,
                "price": 10.99
            }
        ],
        "shipping_address": "123 Test St"
    }
    response = client.post("/api/v1/orders", json=order_data)
    assert response.status_code == 404

def test_get_order(mock_user_service):
    """Test getting order by ID"""
    # Create an order
    order_data = {
        "user_id": "test-user-123",
        "items": [
            {
                "product_id": "prod-1",
                "product_name": "Test Product",
                "quantity": 1,
                "price": 10.99
            }
        ],
        "shipping_address": "123 Test St"
    }
    create_response = client.post("/api/v1/orders", json=order_data)
    assert create_response.status_code == 201
    order_id = create_response.json()["id"]
    
    # Get the order
    response = client.get(f"/api/v1/orders/{order_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == order_id
    assert data["user_id"] == order_data["user_id"]

def test_get_nonexistent_order():
    """Test getting non-existent order"""
    response = client.get("/api/v1/orders/nonexistent-id")
    assert response.status_code == 404

def test_list_orders(mock_user_service):
    """Test listing orders"""
    # Create a few orders
    for i in range(3):
        order_data = {
            "user_id": f"user-{i}",
            "items": [
                {
                    "product_id": f"prod-{i}",
                    "product_name": f"Product {i}",
                    "quantity": 1,
                    "price": 10.99
                }
            ],
            "shipping_address": f"Address {i}"
        }
        client.post("/api/v1/orders", json=order_data)
    
    # List orders
    response = client.get("/api/v1/orders")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3

def test_update_order(mock_user_service):
    """Test updating order"""
    # Create an order
    order_data = {
        "user_id": "test-user-123",
        "items": [
            {
                "product_id": "prod-1",
                "product_name": "Test Product",
                "quantity": 1,
                "price": 10.99
            }
        ],
        "shipping_address": "Original Address"
    }
    create_response = client.post("/api/v1/orders", json=order_data)
    order_id = create_response.json()["id"]
    
    # Update the order
    update_data = {
        "status": "confirmed",
        "shipping_address": "Updated Address"
    }
    response = client.put(f"/api/v1/orders/{order_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "confirmed"
    assert data["shipping_address"] == "Updated Address"

def test_update_order_invalid_status(mock_user_service):
    """Test updating order with invalid status"""
    # Create an order
    order_data = {
        "user_id": "test-user-123",
        "items": [
            {
                "product_id": "prod-1",
                "product_name": "Test Product",
                "quantity": 1,
                "price": 10.99
            }
        ],
        "shipping_address": "Test Address"
    }
    create_response = client.post("/api/v1/orders", json=order_data)
    order_id = create_response.json()["id"]
    
    # Try invalid status
    update_data = {"status": "invalid_status"}
    response = client.put(f"/api/v1/orders/{order_id}", json=update_data)
    assert response.status_code == 400

def test_delete_order(mock_user_service):
    """Test deleting order"""
    # Create an order
    order_data = {
        "user_id": "test-user-123",
        "items": [
            {
                "product_id": "prod-1",
                "product_name": "Test Product",
                "quantity": 1,
                "price": 10.99
            }
        ],
        "shipping_address": "Test Address"
    }
    create_response = client.post("/api/v1/orders", json=order_data)
    order_id = create_response.json()["id"]
    
    # Delete the order
    response = client.delete(f"/api/v1/orders/{order_id}")
    assert response.status_code == 204
    
    # Verify order is deleted
    get_response = client.get(f"/api/v1/orders/{order_id}")
    assert get_response.status_code == 404

def test_get_user_orders(mock_user_service):
    """Test getting orders for a specific user"""
    user_id = "test-user-123"
    
    # Create orders for the user
    for i in range(2):
        order_data = {
            "user_id": user_id,
            "items": [
                {
                    "product_id": f"prod-{i}",
                    "product_name": f"Product {i}",
                    "quantity": 1,
                    "price": 10.99
                }
            ],
            "shipping_address": "Test Address"
        }
        client.post("/api/v1/orders", json=order_data)
    
    # Get user orders
    response = client.get(f"/api/v1/orders/user/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    assert all(order["user_id"] == user_id for order in data)
