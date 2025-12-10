"""
Order Service - Manages order operations
"""
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
import logging
import sys
from datetime import datetime
import uuid
import httpx

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Order Service",
    description="Microservice for order management",
    version="1.0.0"
)

# Configuration
USER_SERVICE_URL = "http://user-service:8000"  # Kubernetes service name
# For local development, use: "http://localhost:8000"

# In-memory storage (replace with database in production)
orders_db = {}

# Pydantic models
class OrderItem(BaseModel):
    product_id: str
    product_name: str
    quantity: int
    price: float

class OrderCreate(BaseModel):
    user_id: str
    items: List[OrderItem]
    shipping_address: str

class OrderResponse(BaseModel):
    id: str
    user_id: str
    items: List[OrderItem]
    shipping_address: str
    total_amount: float
    status: str
    created_at: str
    updated_at: str

class OrderUpdate(BaseModel):
    status: Optional[str] = None
    shipping_address: Optional[str] = None

async def verify_user_exists(user_id: str) -> bool:
    """Verify if user exists in user service"""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{USER_SERVICE_URL}/api/v1/users/{user_id}")
            if response.status_code == 200:
                logger.info(f"User {user_id} verified")
                return True
            else:
                logger.warning(f"User {user_id} not found in user service")
                return False
    except Exception as e:
        logger.error(f"Error verifying user: {str(e)}")
        return False

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for Kubernetes/Docker"""
    logger.info("Health check requested")
    return {
        "status": "healthy",
        "service": "order-service",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/health/ready", tags=["Health"])
async def readiness_check():
    """Readiness probe - check if service is ready to accept traffic"""
    logger.info("Readiness check requested")
    # Check if user service is accessible
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            response = await client.get(f"{USER_SERVICE_URL}/health")
            user_service_healthy = response.status_code == 200
    except Exception as e:
        logger.warning(f"User service not reachable: {str(e)}")
        user_service_healthy = False
    
    return {
        "status": "ready" if user_service_healthy else "degraded",
        "service": "order-service",
        "dependencies": {
            "user-service": "healthy" if user_service_healthy else "unhealthy"
        },
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/health/live", tags=["Health"])
async def liveness_check():
    """Liveness probe - check if service is alive"""
    logger.info("Liveness check requested")
    return {
        "status": "alive",
        "service": "order-service",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/metrics", tags=["Metrics"])
async def metrics():
    """Prometheus metrics endpoint"""
    logger.info("Metrics requested")
    status_counts = {}
    for order in orders_db.values():
        status = order["status"]
        status_counts[status] = status_counts.get(status, 0) + 1
    
    return {
        "total_orders": len(orders_db),
        "orders_by_status": status_counts,
        "service": "order-service"
    }

@app.post("/api/v1/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED, tags=["Orders"])
async def create_order(order: OrderCreate):
    """Create a new order"""
    logger.info(f"Creating order for user: {order.user_id}")
    
    # Verify user exists
    user_exists = await verify_user_exists(order.user_id)
    if not user_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Calculate total amount
    total_amount = sum(item.price * item.quantity for item in order.items)
    
    order_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()
    new_order = {
        "id": order_id,
        "user_id": order.user_id,
        "items": [item.model_dump() for item in order.items],
        "shipping_address": order.shipping_address,
        "total_amount": total_amount,
        "status": "pending",
        "created_at": now,
        "updated_at": now
    }
    orders_db[order_id] = new_order
    
    logger.info(f"Order created successfully with ID: {order_id}, Total: ${total_amount:.2f}")
    return OrderResponse(**new_order)

@app.get("/api/v1/orders", response_model=List[OrderResponse], tags=["Orders"])
async def list_orders(skip: int = 0, limit: int = 100, user_id: Optional[str] = None):
    """List all orders with optional filtering by user_id"""
    logger.info(f"Listing orders: skip={skip}, limit={limit}, user_id={user_id}")
    
    orders = list(orders_db.values())
    
    # Filter by user_id if provided
    if user_id:
        orders = [o for o in orders if o["user_id"] == user_id]
    
    # Apply pagination
    orders = orders[skip:skip + limit]
    
    return [OrderResponse(**order) for order in orders]

@app.get("/api/v1/orders/{order_id}", response_model=OrderResponse, tags=["Orders"])
async def get_order(order_id: str):
    """Get order by ID"""
    logger.info(f"Fetching order with ID: {order_id}")
    
    if order_id not in orders_db:
        logger.warning(f"Order not found: {order_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    return OrderResponse(**orders_db[order_id])

@app.put("/api/v1/orders/{order_id}", response_model=OrderResponse, tags=["Orders"])
async def update_order(order_id: str, order_update: OrderUpdate):
    """Update order information"""
    logger.info(f"Updating order with ID: {order_id}")
    
    if order_id not in orders_db:
        logger.warning(f"Order not found: {order_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    order = orders_db[order_id]
    update_data = order_update.model_dump(exclude_unset=True)
    
    # Validate status if provided
    if "status" in update_data:
        valid_statuses = ["pending", "confirmed", "shipped", "delivered", "cancelled"]
        if update_data["status"] not in valid_statuses:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
            )
    
    order.update(update_data)
    order["updated_at"] = datetime.utcnow().isoformat()
    orders_db[order_id] = order
    
    logger.info(f"Order {order_id} updated successfully")
    return OrderResponse(**order)

@app.delete("/api/v1/orders/{order_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Orders"])
async def delete_order(order_id: str):
    """Delete an order"""
    logger.info(f"Deleting order with ID: {order_id}")
    
    if order_id not in orders_db:
        logger.warning(f"Order not found: {order_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    del orders_db[order_id]
    logger.info(f"Order {order_id} deleted successfully")
    return None

@app.get("/api/v1/orders/user/{user_id}", response_model=List[OrderResponse], tags=["Orders"])
async def get_user_orders(user_id: str):
    """Get all orders for a specific user"""
    logger.info(f"Fetching orders for user: {user_id}")
    
    user_orders = [order for order in orders_db.values() if order["user_id"] == user_id]
    
    return [OrderResponse(**order) for order in user_orders]

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "service": "order-service",
        "version": "1.0.0",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
