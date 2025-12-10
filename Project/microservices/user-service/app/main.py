"""
User Service - Manages user operations
"""
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import logging
import sys
from datetime import datetime
import uuid

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
    title="User Service",
    description="Microservice for user management",
    version="1.0.0"
)

# In-memory storage (replace with database in production)
users_db = {}

# Pydantic models
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: Optional[int] = None

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    age: Optional[int] = None
    created_at: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    age: Optional[int] = None

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for Kubernetes/Docker"""
    logger.info("Health check requested")
    return {
        "status": "healthy",
        "service": "user-service",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/health/ready", tags=["Health"])
async def readiness_check():
    """Readiness probe - check if service is ready to accept traffic"""
    logger.info("Readiness check requested")
    # Add any dependency checks here (database, external services, etc.)
    return {
        "status": "ready",
        "service": "user-service",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/health/live", tags=["Health"])
async def liveness_check():
    """Liveness probe - check if service is alive"""
    logger.info("Liveness check requested")
    return {
        "status": "alive",
        "service": "user-service",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/metrics", tags=["Metrics"])
async def metrics():
    """Prometheus metrics endpoint"""
    logger.info("Metrics requested")
    return {
        "total_users": len(users_db),
        "service": "user-service"
    }

@app.post("/api/v1/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED, tags=["Users"])
async def create_user(user: UserCreate):
    """Create a new user"""
    logger.info(f"Creating user with email: {user.email}")
    
    # Check if user already exists
    for existing_user in users_db.values():
        if existing_user["email"] == user.email:
            logger.warning(f"User with email {user.email} already exists")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists"
            )
    
    user_id = str(uuid.uuid4())
    new_user = {
        "id": user_id,
        "name": user.name,
        "email": user.email,
        "age": user.age,
        "created_at": datetime.utcnow().isoformat()
    }
    users_db[user_id] = new_user
    
    logger.info(f"User created successfully with ID: {user_id}")
    return UserResponse(**new_user)

@app.get("/api/v1/users", response_model=List[UserResponse], tags=["Users"])
async def list_users(skip: int = 0, limit: int = 100):
    """List all users with pagination"""
    logger.info(f"Listing users: skip={skip}, limit={limit}")
    users = list(users_db.values())[skip:skip + limit]
    return [UserResponse(**user) for user in users]

@app.get("/api/v1/users/{user_id}", response_model=UserResponse, tags=["Users"])
async def get_user(user_id: str):
    """Get user by ID"""
    logger.info(f"Fetching user with ID: {user_id}")
    
    if user_id not in users_db:
        logger.warning(f"User not found: {user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse(**users_db[user_id])

@app.put("/api/v1/users/{user_id}", response_model=UserResponse, tags=["Users"])
async def update_user(user_id: str, user_update: UserUpdate):
    """Update user information"""
    logger.info(f"Updating user with ID: {user_id}")
    
    if user_id not in users_db:
        logger.warning(f"User not found: {user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user = users_db[user_id]
    update_data = user_update.model_dump(exclude_unset=True)
    
    # Check email uniqueness if email is being updated
    if "email" in update_data:
        for existing_user in users_db.values():
            if existing_user["id"] != user_id and existing_user["email"] == update_data["email"]:
                logger.warning(f"Email {update_data['email']} already exists")
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email already in use"
                )
    
    user.update(update_data)
    users_db[user_id] = user
    
    logger.info(f"User {user_id} updated successfully")
    return UserResponse(**user)

@app.delete("/api/v1/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Users"])
async def delete_user(user_id: str):
    """Delete a user"""
    logger.info(f"Deleting user with ID: {user_id}")
    
    if user_id not in users_db:
        logger.warning(f"User not found: {user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    del users_db[user_id]
    logger.info(f"User {user_id} deleted successfully")
    return None

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "service": "user-service",
        "version": "1.0.0",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
