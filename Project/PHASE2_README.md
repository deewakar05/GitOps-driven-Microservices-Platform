# Phase 2: CI Pipeline with GitHub Actions

## Overview

Phase 2 implements a comprehensive CI (Continuous Integration) pipeline using GitHub Actions. The pipeline automates testing, building, security scanning, and pushing Docker images to AWS ECR.

## Pipeline Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    GitHub Event Trigger                         │
│  (Push to main/develop or Pull Request)                         │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    JOB 1: TEST                                  │
│  ┌──────────────┐  ┌──────────────┐                          │
│  │ user-service │  │order-service │                          │
│  │   Tests      │  │   Tests      │                          │
│  └──────────────┘  └──────────────┘                          │
│  • Unit Tests                                                  │
│  • Coverage Reports                                            │
│  • Test Artifacts                                              │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    JOB 2: BUILD                                 │
│  ┌──────────────┐  ┌──────────────┐                          │
│  │ user-service │  │order-service │                          │
│  │   Docker     │  │   Docker     │                          │
│  │   Build      │  │   Build      │                          │
│  └──────────────┘  └──────────────┘                          │
│  • Build Docker Images                                         │
│  • Security Scan (Trivy)                                        │
│  • Cache Management                                             │
└────────────────────────┬────────────────────────────────────────┘
                         │
         ┌────────────────┴────────────────┐
         │                                   │
         ▼                                   ▼
┌──────────────────────┐      ┌──────────────────────────────┐
│  JOB 3: PUSH TO ECR  │      │  JOB 4: INTEGRATION TEST     │
│  (main branch only)   │      │  • docker-compose up         │
│  • Tag with SHA       │      │  • Health checks             │
│  • Tag as latest      │      │  • API integration tests      │
│  • Push to ECR        │      │  • Metrics validation        │
└──────────────────────┘      └──────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│              JOB 5: SECURITY SUMMARY                             │
│  • Scan results summary                                         │
│  • Artifact uploads                                            │
└─────────────────────────────────────────────────────────────────┘
```

## Pipeline Features

### ✅ Automated Testing
- **Unit Tests**: Runs pytest for each microservice
- **Coverage Reports**: Generates code coverage reports
- **Parallel Execution**: Tests run in parallel using matrix strategy
- **Artifact Storage**: Test results stored as artifacts

### ✅ Docker Image Building
- **Multi-stage Builds**: Optimized image sizes
- **Build Caching**: Uses GitHub Actions cache for faster builds
- **BuildKit**: Enabled for advanced build features
- **Image Tagging**: Multiple tags (SHA, branch, latest)

### ✅ Security Scanning
- **Trivy Scanner**: Automated vulnerability scanning
- **SARIF Upload**: Results uploaded to GitHub Security tab
- **Fail-safe**: Scans don't fail the build but report issues

### ✅ AWS ECR Integration
- **Conditional Push**: Only pushes on main branch or tags
- **Secure Authentication**: Uses AWS credentials from secrets
- **Image Tagging**: Tags with commit SHA and 'latest'
- **Repository Management**: Separate repositories per service

### ✅ Integration Testing
- **Docker Compose**: Full stack testing
- **Health Checks**: Validates all health endpoints
- **API Testing**: End-to-end API integration tests
- **Metrics Validation**: Verifies metrics endpoints

## Workflow Triggers

### 1. Push Events
```yaml
on:
  push:
    branches: [main, develop]
    paths:
      - 'microservices/**'
      - '.github/workflows/ci.yml'
```

**Triggers when:**
- Code is pushed to `main` or `develop` branches
- Changes are made to microservices or workflow files

### 2. Pull Request Events
```yaml
on:
  pull_request:
    branches: [main, develop]
```

**Triggers when:**
- PR is opened/updated against `main` or `develop`
- Runs tests and builds (but doesn't push to ECR)

### 3. Manual Dispatch
```yaml
on:
  workflow_dispatch:
    inputs:
      service: [all, user-service, order-service]
```

**Allows manual triggering** with service selection

## Required GitHub Secrets

### AWS Credentials
| Secret Name | Description | Example |
|------------|-------------|---------|
| `AWS_ACCESS_KEY_ID` | AWS access key for ECR | `AKIAIOSFODNN7EXAMPLE` |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key | `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY` |
| `AWS_REGION` | AWS region for ECR | `us-east-1` |

### ECR Repository URLs
| Secret Name | Description | Example |
|------------|-------------|---------|
| `ECR_REGISTRY_URL` | Base ECR registry URL | `123456789012.dkr.ecr.us-east-1.amazonaws.com` |
| `ECR_USER_SERVICE_REPOSITORY_URL` | Full user-service repo URL | `123456789012.dkr.ecr.us-east-1.amazonaws.com/microservices-platform/user-service` |
| `ECR_ORDER_SERVICE_REPOSITORY_URL` | Full order-service repo URL | `123456789012.dkr.ecr.us-east-1.amazonaws.com/microservices-platform/order-service` |

## Setting Up GitHub Secrets

### Step 1: Navigate to Repository Settings
1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**

### Step 2: Add AWS Credentials

**AWS_ACCESS_KEY_ID:**
```
Name: AWS_ACCESS_KEY_ID
Value: <your-aws-access-key-id>
```

**AWS_SECRET_ACCESS_KEY:**
```
Name: AWS_SECRET_ACCESS_KEY
Value: <your-aws-secret-access-key>
```

**AWS_REGION:**
```
Name: AWS_REGION
Value: us-east-1
```

### Step 3: Get ECR Repository URLs

After running Terraform (from Phase 1):

```bash
cd infrastructure/terraform/ecr
terraform output
```

You'll get:
- `user_service_repository_url`
- `order_service_repository_url`
- `ecr_registry_url`

### Step 4: Add ECR URLs to Secrets

**ECR_REGISTRY_URL:**
```
Name: ECR_REGISTRY_URL
Value: <from terraform output ecr_registry_url>
```

**ECR_USER_SERVICE_REPOSITORY_URL:**
```
Name: ECR_USER_SERVICE_REPOSITORY_URL
Value: <from terraform output user_service_repository_url>
```

**ECR_ORDER_SERVICE_REPOSITORY_URL:**
```
Name: ECR_ORDER_SERVICE_REPOSITORY_URL
Value: <from terraform output order_service_repository_url>
```

## AWS ECR Login Steps

The workflow uses the official AWS ECR login action:

```yaml
- name: Login to Amazon ECR
  id: login-ecr
  uses: aws-actions/amazon-ecr-login@v2
```

### How It Works

1. **Authentication**: Uses AWS credentials from secrets
2. **Token Retrieval**: Gets temporary ECR login token
3. **Docker Login**: Automatically logs Docker into ECR
4. **Registry Output**: Provides registry URL for tagging

### Manual ECR Login (for testing)

If you need to manually login to ECR:

```bash
# Get login token
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  123456789012.dkr.ecr.us-east-1.amazonaws.com

# Pull an image
docker pull 123456789012.dkr.ecr.us-east-1.amazonaws.com/microservices-platform/user-service:latest
```

## Image Tagging Strategy

### Commit SHA Tag
- **Format**: Full commit SHA (40 characters)
- **Example**: `abc123def456...`
- **Purpose**: Unique identifier for each build
- **Usage**: `user-service:abc123def456...`

### Latest Tag
- **Format**: `latest`
- **Condition**: Only on `main` branch
- **Purpose**: Most recent stable build
- **Usage**: `user-service:latest`

### Branch Tag
- **Format**: Branch name
- **Example**: `develop`, `feature-branch`
- **Purpose**: Track builds per branch
- **Usage**: `user-service:develop`

## Security Best Practices

### 1. Secrets Management
- ✅ Never commit secrets to code
- ✅ Use GitHub Secrets for sensitive data
- ✅ Rotate credentials regularly
- ✅ Use least privilege IAM policies

### 2. Image Security
- ✅ Automated vulnerability scanning with Trivy
- ✅ Scan on every build
- ✅ Report vulnerabilities to GitHub Security tab
- ✅ Use minimal base images

### 3. Access Control
- ✅ IAM user with minimal ECR permissions
- ✅ Separate credentials for CI/CD
- ✅ Enable MFA for AWS account
- ✅ Use AWS IAM roles when possible (future enhancement)

### 4. Workflow Security
- ✅ Only push to ECR on main branch
- ✅ Require PR reviews before merge
- ✅ Use branch protection rules
- ✅ Validate all inputs

## IAM Policy for CI/CD User

Create an IAM user with this policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ecr:GetAuthorizationToken",
        "ecr:BatchCheckLayerAvailability",
        "ecr:GetDownloadUrlForLayer",
        "ecr:BatchGetImage",
        "ecr:PutImage",
        "ecr:InitiateLayerUpload",
        "ecr:UploadLayerPart",
        "ecr:CompleteLayerUpload"
      ],
      "Resource": "*"
    }
  ]
}
```

## Testing the Pipeline

### 1. Test on Pull Request
```bash
# Create a feature branch
git checkout -b test-ci-pipeline

# Make a small change
echo "# Test" >> microservices/user-service/README.md

# Commit and push
git add .
git commit -m "Test CI pipeline"
git push origin test-ci-pipeline

# Create PR on GitHub
```

### 2. Test on Push to Main
```bash
# Merge PR or push directly to main
git checkout main
git merge test-ci-pipeline
git push origin main
```

### 3. Manual Trigger
1. Go to **Actions** tab
2. Select **CI Pipeline**
3. Click **Run workflow**
4. Choose service (or "all")
5. Click **Run workflow**

## Monitoring Pipeline Execution

### View Workflow Runs
1. Go to **Actions** tab in GitHub
2. Click on **CI Pipeline**
3. Select a workflow run
4. View job details and logs

### Check Test Results
- **Test Artifacts**: Download from workflow run artifacts
- **Coverage Reports**: Available in artifacts
- **Test Summary**: Visible in job summary

### Check Security Scans
1. Go to **Security** tab
2. Click **Code scanning alerts**
3. View Trivy scan results

### Verify ECR Push
```bash
# List images in ECR
aws ecr list-images --repository-name microservices-platform/user-service --region us-east-1

# Describe image tags
aws ecr describe-images --repository-name microservices-platform/user-service --region us-east-1
```

## Common Issues and Solutions

### Issue: "Access Denied" when pushing to ECR

**Solution:**
- Verify AWS credentials in GitHub Secrets
- Check IAM user has ECR permissions
- Ensure repository exists in ECR
- Verify AWS_REGION matches repository region

### Issue: Tests fail in CI but pass locally

**Solution:**
- Check Python version matches (3.11)
- Verify all dependencies are in requirements.txt
- Check for environment-specific issues
- Review test logs in Actions tab

### Issue: Docker build fails

**Solution:**
- Check Dockerfile syntax
- Verify build context is correct
- Check for missing files in .dockerignore
- Review build logs for specific errors

### Issue: Integration tests timeout

**Solution:**
- Increase sleep time after docker-compose up
- Check service health endpoints manually
- Verify docker-compose.yml configuration
- Check for port conflicts

### Issue: Security scan shows vulnerabilities

**Solution:**
- Review Trivy scan results
- Update base images to latest versions
- Update dependencies in requirements.txt
- Address critical vulnerabilities first

## Workflow Optimization Tips

### 1. Use Matrix Strategy
- Runs jobs in parallel
- Faster overall execution
- Better resource utilization

### 2. Enable Caching
- Docker layer caching
- Python pip cache
- BuildKit cache

### 3. Conditional Execution
- Skip ECR push on PRs
- Only run expensive jobs when needed
- Use `if` conditions strategically

### 4. Artifact Management
- Upload only necessary artifacts
- Set appropriate retention days
- Clean up old artifacts

## Next Steps

After Phase 2 is complete:

1. ✅ Verify pipeline runs successfully
2. ✅ Check images in ECR
3. ✅ Review security scan results
4. ✅ Test integration tests
5. ⏭️ Proceed to Phase 3: GitOps with ArgoCD

## Verification Checklist

- [ ] GitHub Secrets configured
- [ ] ECR repositories exist
- [ ] Pipeline runs on push
- [ ] Pipeline runs on PR
- [ ] Tests pass
- [ ] Docker images build successfully
- [ ] Security scans complete
- [ ] Images pushed to ECR (on main branch)
- [ ] Integration tests pass
- [ ] Can pull images from ECR

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [AWS ECR Documentation](https://docs.aws.amazon.com/ecr/)
- [Trivy Scanner](https://github.com/aquasecurity/trivy)
- [Docker BuildKit](https://docs.docker.com/build/buildkit/)
