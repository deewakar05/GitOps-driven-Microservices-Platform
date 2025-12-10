# Production-Style Microservices

## Overview

This project contains two production-ready microservices designed for a GitOps-driven DevOps platform:
1. **User Service** - Manages user operations
2. **Order Service** - Manages order operations (depends on User Service)

## Recommended Tech Stack

### Runtime & Framework
- **Python 3.11** - Modern Python with performance improvements
- **FastAPI** - High-performance async web framework with automatic OpenAPI docs
- **Uvicorn** - ASGI server for FastAPI

### Development & Testing
- **pytest** - Testing framework
- **pytest-asyncio** - Async test support
- **httpx** - Async HTTP client for testing and service communication

### Containerization
- **Docker** - Multi-stage builds for optimized images
- **Docker Compose** - Local development orchestration

### Why This Stack?

1. **FastAPI**: 
   - Automatic OpenAPI/Swagger documentation
   - Type hints and validation with Pydantic
   - High performance (comparable to Node.js and Go)
   - Built-in async support
   - Easy to test

2. **Python 3.11**:
   - Latest stable version with performance improvements
   - Good ecosystem for microservices
   - Easy to maintain

3. **Multi-stage Docker builds**:
   - Smaller production images
   - Better security (fewer packages in final image)
   - Faster deployments

## Project Folder Structure

```
project/
├── microservices/
│   ├── user-service/
│   │   ├── app/
│   │   │   ├── __init__.py
│   │   │   ├── main.py          # FastAPI application
│   │   │   └── requirements.txt  # Python dependencies
│   │   ├── tests/
│   │   │   └── test_main.py     # Unit tests
│   │   ├── Dockerfile           # Multi-stage build
│   │   ├── .dockerignore        # Docker build exclusions
│   │   └── README.md            # Service documentation
│   │
│   └── order-service/
│       ├── app/
│       │   ├── __init__.py
│       │   ├── main.py          # FastAPI application
│       │   └── requirements.txt  # Python dependencies
│       ├── tests/
│       │   └── test_main.py     # Unit tests
│       ├── Dockerfile           # Multi-stage build
│       ├── .dockerignore        # Docker build exclusions
│       └── README.md            # Service documentation
│
├── docker-compose.yml           # Local development orchestration
├── .gitignore                   # Git exclusions
└── MICROSERVICES_README.md      # This file
```

## Service Details

### User Service

**Port**: 8000

**Features**:
- User CRUD operations
- Email validation
- Health checks (health, readiness, liveness)
- Prometheus metrics
- Structured logging

**API Endpoints**:
- `GET /health` - Health check
- `GET /health/ready` - Readiness probe
- `GET /health/live` - Liveness probe
- `GET /metrics` - Prometheus metrics
- `POST /api/v1/users` - Create user
- `GET /api/v1/users` - List users (with pagination)
- `GET /api/v1/users/{user_id}` - Get user by ID
- `PUT /api/v1/users/{user_id}` - Update user
- `DELETE /api/v1/users/{user_id}` - Delete user

### Order Service

**Port**: 8001

**Features**:
- Order CRUD operations
- User validation (calls user-service)
- Order status management
- Health checks with dependency checking
- Prometheus metrics
- Structured logging

**API Endpoints**:
- `GET /health` - Health check
- `GET /health/ready` - Readiness probe (checks user-service)
- `GET /health/live` - Liveness probe
- `GET /metrics` - Prometheus metrics
- `POST /api/v1/orders` - Create order
- `GET /api/v1/orders` - List orders (with optional user_id filter)
- `GET /api/v1/orders/{order_id}` - Get order by ID
- `PUT /api/v1/orders/{order_id}` - Update order
- `DELETE /api/v1/orders/{order_id}` - Delete order
- `GET /api/v1/orders/user/{user_id}` - Get all orders for a user

**Order Statuses**: `pending`, `confirmed`, `shipped`, `delivered`, `cancelled`

## Commands to Build and Run Locally

### Prerequisites

```bash
# Check Python version (3.9+ required)
python3 --version

# Check Docker version
docker --version
docker-compose --version
```

### Option 1: Run with Docker Compose (Recommended)

```bash
# From project root directory
cd /Users/deewakarkumar/Devops/project

# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build

# View logs
docker-compose logs -f

# View logs for specific service
docker-compose logs -f user-service
docker-compose logs -f order-service

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### Option 2: Run Services Individually

#### User Service

```bash
# Navigate to user-service directory
cd microservices/user-service

# Install dependencies (if running locally without Docker)
pip install -r app/requirements.txt

# Run locally (development mode)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or build and run with Docker
docker build -t user-service:latest .
docker run -p 8000:8000 user-service:latest
```

#### Order Service

```bash
# Navigate to order-service directory
cd microservices/order-service

# Install dependencies (if running locally without Docker)
pip install -r app/requirements.txt

# IMPORTANT: Update USER_SERVICE_URL in app/main.py to "http://localhost:8000"
# for local development, or set environment variable

# Run locally (development mode)
export USER_SERVICE_URL=http://localhost:8000
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001

# Or build and run with Docker
docker build -t order-service:latest .
docker run -p 8001:8001 -e USER_SERVICE_URL=http://host.docker.internal:8000 order-service:latest
```

### Running Tests

```bash
# User Service Tests
cd microservices/user-service
pip install -r app/requirements.txt
pytest tests/ -v

# Order Service Tests
cd microservices/order-service
pip install -r app/requirements.txt
pytest tests/ -v
```

## Testing the Services

### Using curl

```bash
# Health checks
curl http://localhost:8000/health
curl http://localhost:8001/health

# Create a user
curl -X POST http://localhost:8000/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john.doe@example.com",
    "age": 30
  }'

# Get user ID from response, then create an order
curl -X POST http://localhost:8001/api/v1/orders \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "<user_id_from_above>",
    "items": [
      {
        "product_id": "prod-1",
        "product_name": "Laptop",
        "quantity": 1,
        "price": 999.99
      }
    ],
    "shipping_address": "123 Main St, City, Country"
  }'

# List all orders
curl http://localhost:8001/api/v1/orders

# Get order by ID
curl http://localhost:8001/api/v1/orders/<order_id>
```

### Using API Documentation

FastAPI provides automatic interactive API documentation:

- **User Service**: http://localhost:8000/docs
- **Order Service**: http://localhost:8001/docs

Open these URLs in your browser to explore and test the APIs interactively.

## Production Considerations

### Current Implementation (Development)
- In-memory storage (data lost on restart)
- No authentication/authorization
- No rate limiting
- No database connection pooling
- Basic error handling

### Production Enhancements Needed
1. **Database**: Replace in-memory storage with PostgreSQL/MongoDB
2. **Authentication**: Add JWT tokens or OAuth2
3. **Service Discovery**: Use Kubernetes services or service mesh
4. **Configuration Management**: Use ConfigMaps/Secrets
5. **Logging**: Centralized logging (ELK stack)
6. **Monitoring**: Prometheus + Grafana (covered in Phase 4)
7. **Tracing**: Distributed tracing (Jaeger/Zipkin)
8. **Rate Limiting**: Protect APIs from abuse
9. **Circuit Breaker**: Handle service failures gracefully
10. **Database Migrations**: Alembic or similar

## Common Issues and Solutions

### Issue: Order service can't connect to user service

**Solution**:
- Ensure user-service is running first
- Check network connectivity (use service names in Docker Compose)
- Verify USER_SERVICE_URL environment variable
- For local Docker: use `host.docker.internal:8000`
- For Docker Compose: use `user-service:8000`

### Issue: Port already in use

**Solution**:
```bash
# Find process using port
lsof -i :8000
lsof -i :8001

# Kill the process or change ports in docker-compose.yml
```

### Issue: Docker build fails

**Solution**:
- Check Dockerfile syntax
- Ensure requirements.txt is correct
- Clear Docker cache: `docker system prune -a`
- Rebuild: `docker-compose build --no-cache`

### Issue: Tests fail

**Solution**:
- Ensure all dependencies are installed: `pip install -r app/requirements.txt`
- Run tests from the service directory
- Check Python version (3.9+ required)

### Issue: Import errors

**Solution**:
- Ensure you're running from the correct directory
- Check PYTHONPATH if running locally
- Use Docker for consistent environment

## Next Steps

1. ✅ Services are containerized and tested
2. ✅ Ready for CI/CD pipeline (GitHub Actions)
3. ✅ Ready for Kubernetes deployment
4. ⏭️ Add database persistence
5. ⏭️ Add authentication/authorization
6. ⏭️ Deploy to EKS (Phase 2)
7. ⏭️ Set up ArgoCD (Phase 3)
8. ⏭️ Add observability stack (Phase 4)

## Verification Checklist

- [ ] Both services build successfully
- [ ] Services run with Docker Compose
- [ ] Health checks respond correctly
- [ ] API endpoints work as expected
- [ ] Unit tests pass
- [ ] Services can communicate (order-service → user-service)
- [ ] Logs are structured and readable
- [ ] Metrics endpoints return data
- [ ] API documentation accessible at /docs
