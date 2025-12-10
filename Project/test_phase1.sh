#!/bin/bash

# Phase 1 Testing Script
# This script validates all Phase 1 components

echo "=========================================="
echo "Phase 1 Testing Script"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track test results
TESTS_PASSED=0
TESTS_FAILED=0

test_result() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✓ PASSED${NC}: $2"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}✗ FAILED${NC}: $2"
        ((TESTS_FAILED++))
    fi
}

# Test 1: Check Python version
echo "1. Checking Python version..."
python3 --version > /dev/null 2>&1
test_result $? "Python 3 is installed"

# Test 2: Check project structure
echo ""
echo "2. Checking project structure..."
[ -d "microservices/user-service" ] && [ -d "microservices/order-service" ]
test_result $? "Microservices directories exist"

[ -f "microservices/user-service/Dockerfile" ] && [ -f "microservices/order-service/Dockerfile" ]
test_result $? "Dockerfiles exist"

[ -f "docker-compose.yml" ]
test_result $? "docker-compose.yml exists"

[ -f ".github/workflows/ci.yml" ]
test_result $? "GitHub Actions workflow exists"

[ -d "infrastructure/terraform/ecr" ]
test_result $? "Terraform directory exists"

# Test 3: Validate Python code syntax
echo ""
echo "3. Validating Python code syntax..."
python3 -m py_compile microservices/user-service/app/main.py > /dev/null 2>&1
test_result $? "user-service main.py syntax is valid"

python3 -m py_compile microservices/order-service/app/main.py > /dev/null 2>&1
test_result $? "order-service main.py syntax is valid"

# Test 4: Check dependencies
echo ""
echo "4. Checking dependencies..."
[ -f "microservices/user-service/app/requirements.txt" ]
test_result $? "user-service requirements.txt exists"

[ -f "microservices/order-service/app/requirements.txt" ]
test_result $? "order-service requirements.txt exists"

# Test 5: Run unit tests
echo ""
echo "5. Running unit tests..."

echo "   Testing user-service..."
cd microservices/user-service
if python3 -m pytest tests/test_main.py -v --tb=short > /dev/null 2>&1; then
    test_result 0 "user-service unit tests"
else
    test_result 1 "user-service unit tests"
fi
cd ../..

echo "   Testing order-service..."
cd microservices/order-service
if python3 -m pytest tests/test_main.py -v --tb=short > /dev/null 2>&1; then
    test_result 0 "order-service unit tests"
else
    test_result 1 "order-service unit tests"
fi
cd ../..

# Test 6: Validate Dockerfiles
echo ""
echo "6. Validating Dockerfiles..."
grep -q "FROM python" microservices/user-service/Dockerfile
test_result $? "user-service Dockerfile has FROM instruction"

grep -q "EXPOSE" microservices/user-service/Dockerfile
test_result $? "user-service Dockerfile exposes port"

grep -q "FROM python" microservices/order-service/Dockerfile
test_result $? "order-service Dockerfile has FROM instruction"

grep -q "EXPOSE" microservices/order-service/Dockerfile
test_result $? "order-service Dockerfile exposes port"

# Test 7: Validate Terraform files
echo ""
echo "7. Validating Terraform configuration..."
[ -f "infrastructure/terraform/ecr/main.tf" ]
test_result $? "Terraform main.tf exists"

[ -f "infrastructure/terraform/ecr/variables.tf" ]
test_result $? "Terraform variables.tf exists"

[ -f "infrastructure/terraform/ecr/outputs.tf" ]
test_result $? "Terraform outputs.tf exists"

# Test 8: Validate GitHub Actions workflow
echo ""
echo "8. Validating GitHub Actions workflow..."
grep -q "name:" .github/workflows/ci.yml
test_result $? "GitHub Actions workflow has name"

grep -q "docker build" .github/workflows/ci.yml
test_result $? "GitHub Actions workflow builds Docker images"

grep -q "amazon-ecr-login" .github/workflows/ci.yml
test_result $? "GitHub Actions workflow includes ECR login"

# Test 9: Check Docker availability (optional)
echo ""
echo "9. Checking Docker availability..."
if command -v docker &> /dev/null; then
    docker --version > /dev/null 2>&1
    test_result $? "Docker is installed and accessible"
    echo -e "${YELLOW}  Note: You can test Docker builds with:${NC}"
    echo -e "${YELLOW}    docker-compose build${NC}"
    echo -e "${YELLOW}    docker-compose up${NC}"
else
    echo -e "${YELLOW}⚠ WARNING${NC}: Docker not found in PATH"
    echo -e "${YELLOW}  Install Docker to test container builds${NC}"
fi

# Test 10: Check Terraform availability (optional)
echo ""
echo "10. Checking Terraform availability..."
if command -v terraform &> /dev/null; then
    terraform --version > /dev/null 2>&1
    test_result $? "Terraform is installed and accessible"
    echo -e "${YELLOW}  Note: You can test Terraform with:${NC}"
    echo -e "${YELLOW}    cd infrastructure/terraform/ecr${NC}"
    echo -e "${YELLOW}    terraform init${NC}"
    echo -e "${YELLOW}    terraform plan${NC}"
else
    echo -e "${YELLOW}⚠ WARNING${NC}: Terraform not found in PATH"
    echo -e "${YELLOW}  Install Terraform to provision ECR repositories${NC}"
fi

# Summary
echo ""
echo "=========================================="
echo "Test Summary"
echo "=========================================="
echo -e "${GREEN}Tests Passed: ${TESTS_PASSED}${NC}"
if [ $TESTS_FAILED -gt 0 ]; then
    echo -e "${RED}Tests Failed: ${TESTS_FAILED}${NC}"
    exit 1
else
    echo -e "${GREEN}All tests passed!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Install Docker (if not installed) to test container builds"
    echo "2. Install Terraform (if not installed) to provision ECR"
    echo "3. Configure AWS credentials for ECR access"
    echo "4. Set up GitHub Secrets for CI/CD pipeline"
    exit 0
fi
