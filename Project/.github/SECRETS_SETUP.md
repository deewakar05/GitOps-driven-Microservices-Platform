# GitHub Secrets Setup Guide

## Quick Reference

This guide helps you set up all required GitHub Secrets for the CI/CD pipeline.

## Required Secrets

### AWS Credentials (3 secrets)

1. **AWS_ACCESS_KEY_ID**
   - Description: AWS access key for ECR operations
   - How to get: AWS Console → IAM → Users → Your User → Security Credentials → Create Access Key
   - Format: `AKIAIOSFODNN7EXAMPLE`

2. **AWS_SECRET_ACCESS_KEY**
   - Description: AWS secret access key (paired with access key ID)
   - How to get: Created together with Access Key ID (only shown once!)
   - Format: `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`

3. **AWS_REGION**
   - Description: AWS region where ECR repositories are located
   - Default: `us-east-1`
   - Format: `us-east-1`, `us-west-2`, `eu-west-1`, etc.

### ECR Repository URLs (3 secrets)

4. **ECR_REGISTRY_URL**
   - Description: Base ECR registry URL
   - How to get: Run `terraform output ecr_registry_url` after Phase 1
   - Format: `123456789012.dkr.ecr.us-east-1.amazonaws.com`

5. **ECR_USER_SERVICE_REPOSITORY_URL**
   - Description: Full URL to user-service ECR repository
   - How to get: Run `terraform output user_service_repository_url` after Phase 1
   - Format: `123456789012.dkr.ecr.us-east-1.amazonaws.com/microservices-platform/user-service`

6. **ECR_ORDER_SERVICE_REPOSITORY_URL**
   - Description: Full URL to order-service ECR repository
   - How to get: Run `terraform output order_service_repository_url` after Phase 1
   - Format: `123456789012.dkr.ecr.us-east-1.amazonaws.com/microservices-platform/order-service`

## Step-by-Step Setup

### Step 1: Create AWS IAM User

1. Log in to AWS Console
2. Navigate to **IAM** → **Users**
3. Click **Create user**
4. Name: `github-actions-ci-cd`
5. Select **Provide user access to the console** → **No**
6. Click **Next**

### Step 2: Attach IAM Policy

1. Select **Attach policies directly**
2. Search for `AmazonEC2ContainerRegistryFullAccess`
3. Select it
4. Click **Next** → **Create user**

**OR** Create a custom policy with minimal permissions (see IAM Policy section below)

### Step 3: Create Access Keys

1. Click on the created user
2. Go to **Security credentials** tab
3. Click **Create access key**
4. Select **Command Line Interface (CLI)**
5. Click **Next** → **Create access key**
6. **IMPORTANT**: Copy both:
   - Access key ID
   - Secret access key (shown only once!)

### Step 4: Get ECR Repository URLs

If you haven't run Terraform yet:

```bash
cd infrastructure/terraform/ecr
terraform init
terraform plan
terraform apply
terraform output
```

You'll see output like:
```
user_service_repository_url = "123456789012.dkr.ecr.us-east-1.amazonaws.com/microservices-platform/user-service"
order_service_repository_url = "123456789012.dkr.ecr.us-east-1.amazonaws.com/microservices-platform/order-service"
ecr_registry_url = "123456789012.dkr.ecr.us-east-1.amazonaws.com"
```

### Step 5: Add Secrets to GitHub

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add each secret:

   **Secret 1: AWS_ACCESS_KEY_ID**
   ```
   Name: AWS_ACCESS_KEY_ID
   Secret: <paste your access key ID>
   ```

   **Secret 2: AWS_SECRET_ACCESS_KEY**
   ```
   Name: AWS_SECRET_ACCESS_KEY
   Secret: <paste your secret access key>
   ```

   **Secret 3: AWS_REGION**
   ```
   Name: AWS_REGION
   Secret: us-east-1
   ```

   **Secret 4: ECR_REGISTRY_URL**
   ```
   Name: ECR_REGISTRY_URL
   Secret: 123456789012.dkr.ecr.us-east-1.amazonaws.com
   ```

   **Secret 5: ECR_USER_SERVICE_REPOSITORY_URL**
   ```
   Name: ECR_USER_SERVICE_REPOSITORY_URL
   Secret: 123456789012.dkr.ecr.us-east-1.amazonaws.com/microservices-platform/user-service
   ```

   **Secret 6: ECR_ORDER_SERVICE_REPOSITORY_URL**
   ```
   Name: ECR_ORDER_SERVICE_REPOSITORY_URL
   Secret: 123456789012.dkr.ecr.us-east-1.amazonaws.com/microservices-platform/order-service
   ```

### Step 6: Verify Secrets

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Verify all 6 secrets are listed
3. Check that names match exactly (case-sensitive!)

## Minimal IAM Policy (Recommended)

Instead of full ECR access, use this minimal policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ECRAuthentication",
      "Effect": "Allow",
      "Action": [
        "ecr:GetAuthorizationToken"
      ],
      "Resource": "*"
    },
    {
      "Sid": "ECRImageManagement",
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
      "Resource": [
        "arn:aws:ecr:*:*:repository/microservices-platform/user-service",
        "arn:aws:ecr:*:*:repository/microservices-platform/order-service"
      ]
    }
  ]
}
```

## Testing Secrets

### Test AWS Credentials

```bash
# Configure AWS CLI
aws configure
# Enter your Access Key ID
# Enter your Secret Access Key
# Enter region: us-east-1
# Enter output format: json

# Test authentication
aws sts get-caller-identity

# Should return your account ID and user ARN
```

### Test ECR Access

```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  $(aws sts get-caller-identity --query Account --output text).dkr.ecr.us-east-1.amazonaws.com

# List repositories
aws ecr describe-repositories --region us-east-1

# Should show your repositories
```

### Test GitHub Actions

1. Make a small change to trigger CI
2. Go to **Actions** tab
3. Check if workflow runs without authentication errors
4. Verify ECR push succeeds (on main branch)

## Security Best Practices

### ✅ Do's

- Use separate IAM user for CI/CD (not your personal account)
- Use minimal IAM permissions
- Rotate access keys regularly (every 90 days)
- Enable MFA on AWS account
- Use different credentials for different environments
- Store secrets only in GitHub Secrets (never in code)

### ❌ Don'ts

- Don't commit secrets to repository
- Don't share secrets in chat/email
- Don't use root account credentials
- Don't use overly permissive IAM policies
- Don't hardcode secrets in workflow files
- Don't log secrets in workflow output

## Troubleshooting

### "Access Denied" Error

**Check:**
1. IAM user has correct permissions
2. Repository exists in ECR
3. AWS_REGION matches repository region
4. Access keys are not expired
5. Secrets are correctly named (case-sensitive)

### "Repository Not Found" Error

**Check:**
1. Repository URLs are correct
2. Terraform created repositories successfully
3. Region matches in all configurations
4. Account ID is correct

### "Invalid Credentials" Error

**Check:**
1. Access key ID is correct
2. Secret access key is correct (no extra spaces)
3. Keys are not deactivated
4. IAM user exists and is active

## Updating Secrets

### Update a Secret

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click on the secret name
3. Click **Update**
4. Enter new value
5. Click **Update secret**

### Rotate Access Keys

1. Create new access key in AWS
2. Update secrets in GitHub
3. Test new credentials
4. Delete old access key in AWS

## Verification Checklist

- [ ] AWS IAM user created
- [ ] IAM policy attached (minimal permissions)
- [ ] Access keys created and saved
- [ ] ECR repositories created (via Terraform)
- [ ] All 6 secrets added to GitHub
- [ ] Secret names match exactly
- [ ] AWS credentials tested locally
- [ ] ECR access tested locally
- [ ] GitHub Actions workflow runs successfully

## Next Steps

After secrets are configured:

1. Push code to trigger CI pipeline
2. Verify workflow runs without errors
3. Check ECR for pushed images
4. Review security scan results
5. Proceed to Phase 3: GitOps with ArgoCD
