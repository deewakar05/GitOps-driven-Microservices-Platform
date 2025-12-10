# Phase 1 - Microservice Running Status

**Status:** ✅ **RUNNING**  
**Started:** December 10, 2025  
**Port:** 5001 (http://localhost:5001)

## Service Information

- **Service Name:** User Management Microservice
- **Version:** 1.0.0
- **Status:** Healthy
- **Base URL:** http://localhost:5001

## Available Endpoints

### Health Check
```bash
curl http://localhost:5001/health
```
**Response:**
```json
{
    "status": "healthy",
    "service": "user-microservice",
    "timestamp": "2025-12-10T11:54:10.812129",
    "version": "1.0.0"
}
```

### API Information
```bash
curl http://localhost:5001/
```

### Get All Users
```bash
curl http://localhost:5001/api/users
```

### Get User by ID
```bash
curl http://localhost:5001/api/users/1
```

### Create User
```bash
curl -X POST http://localhost:5001/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com"}'
```

### Update User
```bash
curl -X PUT http://localhost:5001/api/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "John Updated"}'
```

### Delete User
```bash
curl -X DELETE http://localhost:5001/api/users/1
```

## Test Results

✅ Health check endpoint working  
✅ Get all users working  
✅ Create user working  
✅ Get user by ID working  
✅ Update user working  
✅ All CRUD operations functional

## Current Data

The service currently has 3 users:
1. John Doe (john@example.com)
2. Jane Smith (jane@example.com)
3. Bob Updated (bob@example.com)

## Management Commands

### Stop the Service
```bash
pkill -f 'python.*app.py'
```

### Check Service Status
```bash
ps aux | grep "[p]ython.*app.py"
```

### View Logs
```bash
tail -f /tmp/microservice.log
```

### Restart Service
```bash
cd /Users/deewakarkumar/Devops/Project/microservice
PORT=5001 python3 app.py > /tmp/microservice.log 2>&1 &
```

## Next Steps

The microservice is running successfully and ready for:
- Phase 2: CI/CD pipeline setup with GitHub Actions
- Docker containerization testing
- Integration with monitoring tools (Phase 5)

---

**Note:** The service is running on port 5001 because port 5000 is typically used by macOS AirPlay Receiver. To use port 5000, disable AirPlay Receiver in System Preferences.

