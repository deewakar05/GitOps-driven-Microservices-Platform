# Order Service

Microservice for managing orders.

## Features

- RESTful API for order CRUD operations
- Integration with user service for user validation
- Health check endpoints (health, readiness, liveness)
- Structured logging
- Prometheus metrics endpoint
- Unit tests
- Docker containerization

## API Endpoints

- `GET /health` - Health check
- `GET /health/ready` - Readiness probe (checks user service dependency)
- `GET /health/live` - Liveness probe
- `GET /metrics` - Prometheus metrics
- `POST /api/v1/orders` - Create order
- `GET /api/v1/orders` - List orders (with optional user_id filter)
- `GET /api/v1/orders/{order_id}` - Get order by ID
- `PUT /api/v1/orders/{order_id}` - Update order
- `DELETE /api/v1/orders/{order_id}` - Delete order
- `GET /api/v1/orders/user/{user_id}` - Get all orders for a user

## Order Status

Valid statuses: `pending`, `confirmed`, `shipped`, `delivered`, `cancelled`

## Local Development

```bash
# Install dependencies
pip install -r app/requirements.txt

# Run the service
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001

# Run tests
pytest tests/ -v

# Access API docs
# Open http://localhost:8001/docs
```

## Docker

```bash
# Build image
docker build -t order-service:latest .

# Run container
docker run -p 8001:8001 order-service:latest
```

## Dependencies

This service depends on the user-service. Make sure user-service is running and accessible.
