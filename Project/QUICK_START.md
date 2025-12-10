# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Start Services with Docker Compose

```bash
cd /Users/deewakarkumar/Devops/project
docker-compose up --build
```

This will:
- Build both microservices
- Start user-service on port 8000
- Start order-service on port 8001
- Set up networking between services

### Step 2: Verify Services are Running

Open in your browser:
- **User Service API Docs**: http://localhost:8000/docs
- **Order Service API Docs**: http://localhost:8001/docs

Or test with curl:
```bash
# Health checks
curl http://localhost:8000/health
curl http://localhost:8001/health
```

### Step 3: Test the Services

#### Create a User
```bash
curl -X POST http://localhost:8000/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john.doe@example.com",
    "age": 30
  }'
```

Save the `id` from the response.

#### Create an Order
```bash
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
```

## 📚 Full Documentation

- **Microservices Details**: See [MICROSERVICES_README.md](./MICROSERVICES_README.md)
- **Phase 1 Setup**: See [PHASE1_README.md](./PHASE1_README.md)

## 🧪 Run Tests

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

## 🛑 Stop Services

```bash
docker-compose down
```

## 📊 View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f user-service
docker-compose logs -f order-service
```
