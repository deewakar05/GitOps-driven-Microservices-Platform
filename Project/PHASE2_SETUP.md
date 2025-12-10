# Phase 2 Setup Guide

## Quick Start

### 1. Push Code to GitHub

```bash
# Initialize git repository (if not already done)
git init
git add .
git commit -m "Phase 1: Microservice implementation"

# Add your GitHub repository
git remote add origin https://github.com/your-username/your-repo.git
git branch -M main
git push -u origin main
```

### 2. Configure GitHub Secrets

For ECR push to work, configure AWS credentials:

1. Go to your GitHub repository
2. Navigate to: **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add one of these options:

#### Option A: IAM Role (Recommended)
- **Name**: `AWS_ROLE_ARN`
- **Value**: `arn:aws:iam::ACCOUNT_ID:role/GitHubActionsRole`

#### Option B: Access Keys (Less Secure)
- **Name**: `AWS_ACCESS_KEY_ID`
- **Value**: Your AWS access key
- **Name**: `AWS_SECRET_ACCESS_KEY`
- **Value**: Your AWS secret key

### 3. Create AWS ECR Repository

```bash
# Set your AWS region
export AWS_REGION=us-east-1

# Create ECR repository
aws ecr create-repository \
  --repository-name user-microservice \
  --region $AWS_REGION \
  --image-scanning-configuration scanOnPush=true \
  --encryption-configuration encryptionType=AES256

# Get repository URI
aws ecr describe-repositories \
  --repository-names user-microservice \
  --region $AWS_REGION \
  --query 'repositories[0].repositoryUri' \
  --output text
```

### 4. Update Workflow Configuration (if needed)

If your ECR repository name or region differs, edit `.github/workflows/cd.yml`:

```yaml
env:
  AWS_REGION: your-region          # Change if needed
  ECR_REPOSITORY: your-repo-name   # Change if needed
```

### 5. Test the Workflows

#### Test CI Workflow
```bash
# Make a small change
echo "# Test" >> microservice/README.md
git add .
git commit -m "Test CI workflow"
git push
```

Then check: **Actions** tab → **CI - Test and Build**

#### Test CD Workflow
```bash
# Push to main branch
git checkout main
git push origin main
```

Then check: **Actions** tab → **CD - Build and Push to ECR**

## Workflow Behavior

### CI Workflow (`ci.yml`)
- **Triggers**: Push/PR to `main` or `develop`
- **Runs**: Tests, linting, Docker build
- **Duration**: ~2-3 minutes

### CD Workflow (`cd.yml`)
- **Triggers**: Push to `main` or version tag (`v*`)
- **Runs**: Build Docker image, push to ECR
- **Duration**: ~3-5 minutes

### Manual Workflow
- **Triggers**: Manual from GitHub UI
- **Options**: Environment, run tests, build image
- **Use Case**: Staging/production deployments

## Verification

### Check Workflow Status
1. Go to **Actions** tab in GitHub
2. Click on a workflow run
3. Check all jobs are green ✅

### Verify ECR Push
```bash
# List images in ECR
aws ecr list-images \
  --repository-name user-microservice \
  --region us-east-1
```

### Test Docker Image Locally
```bash
# Pull from ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

docker pull YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/user-microservice:latest

# Run locally
docker run -p 5000:5000 \
  YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/user-microservice:latest
```

## Troubleshooting

### Workflow Not Running
- ✅ Check branch name matches trigger
- ✅ Verify workflow files are in `.github/workflows/`
- ✅ Check YAML syntax (no tabs, proper indentation)

### Tests Failing
```bash
# Run tests locally first
cd microservice
python3 test_app.py
```

### ECR Push Failing
- ✅ Verify AWS credentials in GitHub Secrets
- ✅ Check IAM permissions
- ✅ Verify ECR repository exists
- ✅ Check AWS region matches

### Docker Build Failing
```bash
# Test Dockerfile locally
cd microservice
docker build -t test .
docker run -p 5000:5000 test
```

## IAM Policy Example

Create an IAM policy for ECR access:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ecr:GetAuthorizationToken"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "ecr:BatchCheckLayerAvailability",
        "ecr:GetDownloadUrlForLayer",
        "ecr:BatchGetImage",
        "ecr:PutImage",
        "ecr:InitiateLayerUpload",
        "ecr:UploadLayerPart",
        "ecr:CompleteLayerUpload"
      ],
      "Resource": "arn:aws:ecr:*:*:repository/user-microservice"
    }
  ]
}
```

## Next Steps

✅ Phase 2 complete!  
🚀 Ready for Phase 3: Terraform EKS provisioning

## Support

- Check workflow logs in GitHub Actions
- Review `.github/workflows/README.md` for detailed documentation
- See `microservice/PHASE2_README.md` for Phase 2 overview

