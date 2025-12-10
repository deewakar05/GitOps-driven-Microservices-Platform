"""
Sample Microservice - User Management API
A simple REST API microservice for Phase 1 of the DevOps project.
"""

from flask import Flask, jsonify, request
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# In-memory storage (for demo purposes)
users_db = {
    1: {"id": 1, "name": "John Doe", "email": "john@example.com", "created_at": "2025-11-01"},
    2: {"id": 2, "name": "Jane Smith", "email": "jane@example.com", "created_at": "2025-11-02"}
}

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        "status": "healthy",
        "service": "user-microservice",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }), 200

@app.route('/api/users', methods=['GET'])
def get_users():
    """Get all users"""
    logger.info("GET /api/users - Fetching all users")
    return jsonify({
        "users": list(users_db.values()),
        "count": len(users_db)
    }), 200

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get a specific user by ID"""
    logger.info(f"GET /api/users/{user_id} - Fetching user")
    if user_id not in users_db:
        return jsonify({"error": "User not found"}), 404
    return jsonify(users_db[user_id]), 200

@app.route('/api/users', methods=['POST'])
def create_user():
    """Create a new user"""
    logger.info("POST /api/users - Creating new user")
    data = request.get_json()
    
    if not data or not data.get('name') or not data.get('email'):
        return jsonify({"error": "Name and email are required"}), 400
    
    new_id = max(users_db.keys()) + 1 if users_db else 1
    new_user = {
        "id": new_id,
        "name": data['name'],
        "email": data['email'],
        "created_at": datetime.now().strftime("%Y-%m-%d")
    }
    users_db[new_id] = new_user
    
    logger.info(f"Created user with ID: {new_id}")
    return jsonify(new_user), 201

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update an existing user"""
    logger.info(f"PUT /api/users/{user_id} - Updating user")
    if user_id not in users_db:
        return jsonify({"error": "User not found"}), 404
    
    data = request.get_json()
    if data:
        if 'name' in data:
            users_db[user_id]['name'] = data['name']
        if 'email' in data:
            users_db[user_id]['email'] = data['email']
    
    return jsonify(users_db[user_id]), 200

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user"""
    logger.info(f"DELETE /api/users/{user_id} - Deleting user")
    if user_id not in users_db:
        return jsonify({"error": "User not found"}), 404
    
    deleted_user = users_db.pop(user_id)
    return jsonify({"message": "User deleted", "user": deleted_user}), 200

@app.route('/', methods=['GET'])
def index():
    """Root endpoint"""
    return jsonify({
        "message": "User Management Microservice",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "get_users": "GET /api/users",
            "get_user": "GET /api/users/<id>",
            "create_user": "POST /api/users",
            "update_user": "PUT /api/users/<id>",
            "delete_user": "DELETE /api/users/<id>"
        }
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    logger.info(f"Starting microservice on {host}:{port}")
    app.run(host=host, port=port, debug=False)

