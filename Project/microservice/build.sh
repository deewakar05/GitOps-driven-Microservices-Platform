#!/bin/bash

# Build script for Phase 1 - Microservice Docker Image

echo "Building Docker image for user-microservice..."
docker build -t user-microservice:latest .

if [ $? -eq 0 ]; then
    echo "✅ Docker image built successfully!"
    echo ""
    echo "To run the container:"
    echo "  docker run -d -p 5000:5000 --name user-service user-microservice:latest"
    echo ""
    echo "To test the service:"
    echo "  curl http://localhost:5000/health"
else
    echo "❌ Docker build failed!"
    exit 1
fi

