# GitHub Actions Workflows

This directory contains CI/CD workflows for the DevOps project.

## Workflows

### 1. CI Workflow (`ci.yml`)
**Trigger:** Push/PR to `main` or `develop` branches

**Jobs:**
- **test**: Runs unit tests using Python
- **lint**: Performs code quality checks (flake8, pylint)
- **docker-build**: Builds and tests Docker image

**Features:**
- Automated testing on every push/PR
- Code quality checks
- Docker image validation
- Image size reporting

### 2. CD Workflow (`cd.yml`)
**Trigger:** Push to `main` branch or version tags (`v*`)

**Jobs:**
- **build-and-push**: Builds Docker image and pushes to AWS ECR
- **build-local-test**: Builds Docker image for testing (non-main branches)

**Features:**
- Automatic Docker image building
- Push to AWS ECR (requires AWS credentials)
- Image tagging with commit SHA or version tag
- Health check validation

### 3. Manual Workflow (`workflow_dispatch.yml`)
**Trigger:** Manual trigger from GitHub Actions UI

**Features:**
- Customizable deployment environment
- Optional test execution
- Optional Docker image building
- Useful for staging/production deployments

## Setup Instructions

### 1. AWS ECR Setup (for CD workflow)

1. Create an ECR repository:
```bash
aws ecr create-repository --repository-name user-microservice --region us-east-1
```

2. Configure GitHub Secrets:
   - Go to Repository Settings → Secrets and variables → Actions
   - Add the following secrets:
     - `AWS_ROLE_ARN`: ARN of IAM role for ECR access
     - Or use `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` (less secure)

### 2. Update ECR Repository Name

If your ECR repository name differs, update the `ECR_REPOSITORY` environment variable in `cd.yml`:

```yaml
env:
  ECR_REPOSITORY: your-repository-name
```

### 3. Update AWS Region

Modify the `AWS_REGION` in `cd.yml` if needed:

```yaml
env:
  AWS_REGION: your-preferred-region
```

## Workflow Status Badge

Add this to your README.md to show workflow status:

```markdown
![CI](https://github.com/your-username/your-repo/actions/workflows/ci.yml/badge.svg)
![CD](https://github.com/your-username/your-repo/actions/workflows/cd.yml/badge.svg)
```

## Testing Workflows Locally

### Using Act (optional)

Install [act](https://github.com/nektos/act) to test workflows locally:

```bash
# Test CI workflow
act push

# Test specific job
act -j test

# Test with secrets
act push --secret-file .secrets
```

## Workflow Triggers

| Workflow | Trigger | When |
|----------|---------|------|
| CI | Push/PR | On every push or PR to main/develop |
| CD | Push to main | On push to main branch |
| CD | Version tag | On tag push (v*.*.*) |
| Manual | Workflow dispatch | Manual trigger from GitHub UI |

## Troubleshooting

### CI Workflow Fails

1. Check Python version compatibility
2. Verify all dependencies in `requirements.txt`
3. Ensure tests pass locally: `python test_app.py`

### CD Workflow Fails

1. Verify AWS credentials are configured correctly
2. Check ECR repository exists and is accessible
3. Ensure IAM role has ECR push permissions
4. Verify AWS region matches your ECR repository region

### Docker Build Fails

1. Test Dockerfile locally: `docker build -t test .`
2. Check Dockerfile syntax
3. Verify all files are present in the repository

## Phase 2 Status

✅ CI pipeline configured  
✅ Automated testing implemented  
✅ Docker build automation  
✅ ECR push configuration  
✅ Manual workflow trigger  

**Phase 2 Complete!** Ready for Phase 3 (Terraform EKS provisioning).

