# Phase 2: CI/CD Pipeline with GitHub Actions

**Status:** ✅ **COMPLETE**

## Overview

Phase 2 implements automated CI/CD pipeline using GitHub Actions for:
- Automated testing on every push/PR
- Docker image building
- Push to AWS ECR (Container Registry)
- Code quality checks

## What Was Implemented

### 1. CI Workflow (`.github/workflows/ci.yml`)
- **Automated Testing**: Runs unit tests on every push/PR
- **Code Quality**: Linting with flake8 and pylint
- **Docker Build**: Builds and validates Docker image
- **Health Checks**: Tests Docker container functionality

### 2. CD Workflow (`.github/workflows/cd.yml`)
- **ECR Push**: Automatically pushes Docker images to AWS ECR
- **Image Tagging**: Tags images with commit SHA or version tags
- **Multi-stage**: Different behavior for main branch vs others
- **Health Validation**: Tests container before pushing

### 3. Manual Workflow (`.github/workflows/workflow_dispatch.yml`)
- **Manual Trigger**: Allows manual deployment from GitHub UI
- **Environment Selection**: Choose staging or production
- **Flexible Options**: Toggle tests and builds

## Workflow Features

### CI Pipeline
```
Push/PR → Checkout → Setup Python → Install Dependencies → 
Run Tests → Lint Code → Build Docker → Test Container
```

### CD Pipeline
```
Push to main → Checkout → AWS Login → Build Image → 
Tag Image → Push to ECR → Output Image URI
```

## Setup Requirements

### GitHub Secrets (Required for ECR Push)

1. Go to: Repository → Settings → Secrets and variables → Actions
2. Add secrets:
   - `AWS_ROLE_ARN`: IAM role ARN for ECR access (recommended)
   - OR `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` (alternative)

### AWS ECR Repository

Create ECR repository:
```bash
aws ecr create-repository \
  --repository-name user-microservice \
  --region us-east-1
```

### IAM Permissions

The IAM role/user needs:
- `ecr:GetAuthorizationToken`
- `ecr:BatchCheckLayerAvailability`
- `ecr:GetDownloadUrlForLayer`
- `ecr:BatchGetImage`
- `ecr:PutImage`
- `ecr:InitiateLayerUpload`
- `ecr:UploadLayerPart`
- `ecr:CompleteLayerUpload`

## Testing the Workflows

### Test CI Workflow
1. Make a change to the code
2. Push to `develop` or `main` branch
3. Check Actions tab in GitHub
4. Verify all jobs pass

### Test CD Workflow
1. Push to `main` branch
2. Check Actions tab
3. Verify image is pushed to ECR
4. Check ECR console for new image

### Manual Trigger
1. Go to Actions tab
2. Select "Manual Workflow Trigger"
3. Click "Run workflow"
4. Select options and run

## Workflow Status

| Workflow | Status | Trigger |
|----------|--------|---------|
| CI | ✅ Active | Push/PR to main/develop |
| CD | ✅ Active | Push to main or version tag |
| Manual | ✅ Active | Manual trigger |

## Expected Outcomes

✅ **Automated build and testing** - Complete  
✅ **Docker image automation** - Complete  
✅ **ECR integration** - Complete  
✅ **Code quality checks** - Complete  

## Next Steps

Phase 2 is complete! Ready for:
- **Phase 3**: Provision EKS using Terraform
- **Phase 4**: Implement GitOps with ArgoCD

## Troubleshooting

### Workflow Not Triggering
- Check branch name matches workflow trigger
- Verify workflow file is in `.github/workflows/` directory
- Check workflow file syntax (YAML)

### Tests Failing
- Run tests locally: `python test_app.py`
- Check Python version compatibility
- Verify dependencies are installed

### ECR Push Failing
- Verify AWS credentials are correct
- Check ECR repository exists
- Verify IAM permissions
- Check AWS region matches

### Docker Build Failing
- Test locally: `docker build -t test .`
- Check Dockerfile syntax
- Verify all files are present

## Files Created

```
.github/
└── workflows/
    ├── ci.yml                    # CI workflow
    ├── cd.yml                    # CD workflow
    ├── workflow_dispatch.yml     # Manual workflow
    └── README.md                 # Workflow documentation
```

## Phase 2 Checklist

- [x] CI workflow created
- [x] CD workflow created
- [x] Manual workflow created
- [x] Automated testing configured
- [x] Docker build automation
- [x] ECR push configuration
- [x] Code quality checks
- [x] Documentation created

**Phase 2 Status: ✅ COMPLETE**

