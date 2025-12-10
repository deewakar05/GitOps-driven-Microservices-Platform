# Phase 1: Foundation Setup

## Overview

Phase 1 establishes the foundation of our GitOps-driven microservices platform. We'll create:
1. A sample microservice application
2. Docker containerization
3. GitHub Actions CI pipeline
4. Terraform configuration for AWS ECR
5. Basic project structure

## Folder Structure

```
project/
├── microservices/
│   ├── user-service/
│   │   ├── app/
│   │   │   ├── __init__.py
│   │   │   ├── main.py
│   │   │   └── requirements.txt
│   │   ├── tests/
│   │   │   └── test_main.py
│   │   ├── Dockerfile
│   │   ├── .dockerignore
│   │   └── README.md
│   └── order-service/
│       ├── app/
│       │   ├── __init__.py
│       │   ├── main.py
│       │   └── requirements.txt
│       ├── tests/
│       │   └── test_main.py
│       ├── Dockerfile
│       ├── .dockerignore
│       └── README.md
├── infrastructure/
│   └── terraform/
│       └── ecr/
│           ├── main.tf
│           ├── variables.tf
│           ├── outputs.tf
│           └── README.md
├── .github/
│   └── workflows/
│       └── ci.yml
├── docker-compose.yml
├── .gitignore
├── test_phase1.sh
└── README.md
```

## Components Explained

### 1. Microservices
Two production-ready microservices:
- **User Service**: Manages user operations (CRUD, health checks, metrics)
- **Order Service**: Manages order operations with user service integration
Both services include:
- Health check endpoints (health, readiness, liveness)
- Metrics endpoint (for Prometheus)
- RESTful API endpoints
- Structured logging
- Unit tests

### 2. Docker Configuration
- **Dockerfile**: Multi-stage build for optimized image size
- **.dockerignore**: Excludes unnecessary files from build context
- **docker-compose.yml**: Local development environment

### 3. GitHub Actions CI
Automated pipeline that:
- Builds Docker image
- Runs tests
- Pushes to AWS ECR
- Tags images with commit SHA and branch name

### 4. Terraform for ECR
Infrastructure as Code to provision:
- ECR repository
- Lifecycle policies
- Repository policies

## Prerequisites

Before starting, ensure you have:

1. **AWS Account** with appropriate permissions
2. **AWS CLI** installed and configured
   ```bash
   aws --version
   aws configure
   ```
3. **Terraform** installed (>= 1.0)
   ```bash
   terraform --version
   ```
4. **Docker** installed and running
   ```bash
   docker --version
   ```
5. **Python 3.9+** (for local development)
   ```bash
   python3 --version
   ```
6. **GitHub Repository** with Actions enabled

## AWS Setup

1. Create an IAM user for CI/CD with these permissions:
   - `AmazonEC2ContainerRegistryFullAccess`
   - Or create a custom policy with ECR permissions

2. Configure AWS credentials:
   ```bash
   aws configure
   # Enter your Access Key ID
   # Enter your Secret Access Key
   # Enter your default region (e.g., us-east-1)
   # Enter default output format (json)
   ```

3. Add AWS credentials to GitHub Secrets:
   - Go to your GitHub repository
   - Settings → Secrets and variables → Actions
   - Add secrets:
     - `AWS_ACCESS_KEY_ID`
     - `AWS_SECRET_ACCESS_KEY`
     - `AWS_REGION` (e.g., us-east-1)
     - `ECR_REPOSITORY_NAME` (e.g., microservices-platform)

## Commands to Run

### Step 1: Provision ECR Repository with Terraform

```bash
cd infrastructure/terraform/ecr

# Initialize Terraform
terraform init

# Review the execution plan
terraform plan

# Apply the configuration
terraform apply

# Note the repository URL from outputs
terraform output ecr_repository_url
```

### Step 2: Configure GitHub Secrets

Add the ECR repository URL to GitHub Secrets:
- `ECR_REPOSITORY_URL`: Output from terraform apply

### Step 3: Test Locally

```bash
# Build and run with docker-compose (recommended)
docker-compose up --build

# Or build individual services
cd microservices/user-service
docker build -t user-service:latest .
docker run -p 8000:8000 user-service:latest

cd ../order-service
docker build -t order-service:latest .
docker run -p 8001:8001 order-service:latest

# Test the services
curl http://localhost:8000/health
curl http://localhost:8001/health
```

### Step 4: Test with Docker Compose

```bash
# From project root
docker-compose up -d

# Check logs
docker-compose logs -f

# Test endpoints
curl http://localhost:8000/health
curl http://localhost:8001/health
curl http://localhost:8000/metrics
curl http://localhost:8001/metrics

# Stop services
docker-compose down
```

### Step 5: Trigger CI Pipeline

```bash
# Commit and push to trigger GitHub Actions
git add .
git commit -m "Phase 1: Foundation setup"
git push origin main
```

Check GitHub Actions tab to see the pipeline execution.

## Common Mistakes and How to Avoid Them

### 1. **AWS Credentials Not Configured**
**Mistake**: GitHub Actions fails with "Access Denied" errors
**Solution**: 
- Verify AWS credentials in GitHub Secrets
- Ensure IAM user has ECR permissions
- Check AWS region matches in all configurations

### 2. **ECR Repository Not Created First**
**Mistake**: CI pipeline fails because ECR repository doesn't exist
**Solution**: 
- Always run `terraform apply` before pushing code
- Verify repository exists: `aws ecr describe-repositories`

### 3. **Docker Build Context Issues**
**Mistake**: Docker build includes unnecessary files, making it slow
**Solution**: 
- Use `.dockerignore` to exclude files
- Keep Dockerfile in the service directory
- Use multi-stage builds

### 4. **Wrong Image Tags**
**Mistake**: Images overwrite each other or can't be tracked
**Solution**: 
- Use commit SHA for unique tags
- Use branch names for environment-specific tags
- Never use `latest` in production

### 5. **Terraform State Not Managed**
**Mistake**: State file conflicts in team environments
**Solution**: 
- Use remote state (S3 backend) - we'll add this in Phase 2
- For now, don't commit `terraform.tfstate` (it's in .gitignore)

### 6. **Python Dependencies Not Pinned**
**Mistake**: Builds are inconsistent across environments
**Solution**: 
- Pin exact versions in `requirements.txt`
- Use `pip freeze` to generate requirements
- Review and update dependencies regularly

### 7. **Missing Health Checks**
**Mistake**: Kubernetes can't determine if service is ready
**Solution**: 
- Always implement `/health` endpoint
- Return proper HTTP status codes
- Include dependency checks

### 8. **Large Docker Images**
**Mistake**: Slow builds and deployments
**Solution**: 
- Use multi-stage builds
- Use Alpine-based images when possible
- Remove build dependencies in final stage
- Use `.dockerignore`

## Verification Checklist

- [ ] ECR repository created and accessible
- [ ] Docker image builds successfully locally
- [ ] Service responds to health checks
- [ ] GitHub Actions workflow runs without errors
- [ ] Image pushed to ECR successfully
- [ ] Can pull image from ECR: `aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <ecr-url>`
- [ ] Terraform outputs are correct

## Next Steps

Once Phase 1 is complete and verified:
1. Review all components
2. Test the complete CI pipeline
3. Confirm ECR repository contains the image
4. Proceed to Phase 2: Infrastructure Provisioning

## Troubleshooting

### GitHub Actions Fails
- Check workflow logs in GitHub Actions tab
- Verify all secrets are set correctly
- Ensure AWS credentials have correct permissions

### Terraform Errors
- Run `terraform init` again if modules change
- Check AWS credentials: `aws sts get-caller-identity`
- Verify region is correct

### Docker Build Fails
- Check Dockerfile syntax
- Verify base image exists
- Check network connectivity for pulling base images

### ECR Login Issues
- Get login token: `aws ecr get-login-password --region <region>`
- Login manually: `docker login -u AWS -p <token> <ecr-url>`
- Check repository exists: `aws ecr describe-repositories`
