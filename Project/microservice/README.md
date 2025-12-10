# User Management Microservice

This is a sample microservice created for **Phase 1** of the DevOps Project: GitOps-driven Microservices Platform with Full Observability.

## Overview

A simple REST API microservice built with Flask that demonstrates:
- RESTful API endpoints
- Health check endpoint for monitoring
- Containerization with Docker
- Basic logging and error handling

## Features

- **Health Check**: `/health` endpoint for service monitoring
- **User Management**: CRUD operations for users
  - GET `/api/users` - List all users
  - GET `/api/users/<id>` - Get a specific user
  - POST `/api/users` - Create a new user
  - PUT `/api/users/<id>` - Update a user
  - DELETE `/api/users/<id>` - Delete a user

## Prerequisites

- Python 3.11+
- Docker (for containerization)

## Local Development

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
python app.py
```

The service will start on `http://localhost:5000`

### Run Tests

```bash
python test_app.py
```

## Docker Usage

### Build the Docker Image

```bash
docker build -t user-microservice:latest .
```

### Run the Container

```bash
docker run -d -p 5000:5000 --name user-service user-microservice:latest
```

### Test the Service

```bash
# Health check
curl http://localhost:5000/health

# Get all users
curl http://localhost:5000/api/users

# Create a user
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice", "email": "alice@example.com"}'
```

### Stop and Remove Container

```bash
docker stop user-service
docker rm user-service
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check endpoint |
| GET | `/` | API information |
| GET | `/api/users` | Get all users |
| GET | `/api/users/<id>` | Get user by ID |
| POST | `/api/users` | Create new user |
| PUT | `/api/users/<id>` | Update user |
| DELETE | `/api/users/<id>` | Delete user |

## Environment Variables

- `PORT`: Server port (default: 5000)
- `HOST`: Server host (default: 0.0.0.0)

## Project Structure

```
microservice/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── Dockerfile         # Docker configuration
├── .dockerignore      # Docker ignore file
├── test_app.py        # Unit tests
└── README.md          # This file
```

## Next Steps (Phase 2)

This microservice will be integrated with:
- GitHub Actions for CI/CD
- AWS ECR for container registry
- Automated testing and deployment

## Notes

- This is a demo microservice with in-memory storage
- For production use, integrate with a proper database
- Add authentication and authorization as needed
- Implement proper error handling and validation

