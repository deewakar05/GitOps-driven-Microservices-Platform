# User Service

Microservice for managing users.

## Features

- RESTful API for user CRUD operations
- Health check endpoints (health, readiness, liveness)
- Structured logging
- Prometheus metrics endpoint
- Unit tests
- Docker containerization

## API Endpoints

- `GET /health` - Health check
- `GET /health/ready` - Readiness probe
- `GET /health/live` - Liveness probe
- `GET /metrics` - Prometheus metrics
- `POST /api/v1/users` - Create user
- `GET /api/v1/users` - List users
- `GET /api/v1/users/{user_id}` - Get user by ID
- `PUT /api/v1/users/{user_id}` - Update user
- `DELETE /api/v1/users/{user_id}` - Delete user

## Local Development

```bash
# Install dependencies
pip install -r app/requirements.txt

# Run the service
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
pytest tests/ -v

# Access API docs
# Open http://localhost:8000/docs
```

## Docker

```bash
# Build image
docker build -t user-service:latest .

# Run container
docker run -p 8000:8000 user-service:latest
```
