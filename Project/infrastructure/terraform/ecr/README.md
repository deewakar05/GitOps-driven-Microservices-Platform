# ECR Terraform Configuration

This directory contains Terraform configuration to provision AWS ECR repositories for the microservices.

## Resources Created

- **user-service ECR repository** - Container registry for user-service
- **order-service ECR repository** - Container registry for order-service
- **Lifecycle policies** - Automatically clean up old images (keeps last 10)

## Usage

### Prerequisites

1. AWS CLI configured with appropriate credentials
2. Terraform installed (>= 1.0)
3. IAM permissions for ECR operations

### Initialize Terraform

```bash
terraform init
```

### Plan Changes

```bash
terraform plan
```

### Apply Configuration

```bash
terraform apply
```

You'll be prompted to confirm. Type `yes` to proceed.

### View Outputs

```bash
terraform output
```

This will show:
- `user_service_repository_url` - Full URL for user-service repository
- `order_service_repository_url` - Full URL for order-service repository
- `ecr_registry_url` - Base ECR registry URL

### Destroy Resources

```bash
terraform destroy
```

⚠️ **Warning**: This will delete all images in the repositories!

## Variables

You can override default values:

```bash
terraform apply -var="aws_region=us-west-2" -var="environment=prod"
```

Or create a `terraform.tfvars` file:

```hcl
aws_region            = "us-east-1"
ecr_repository_prefix = "my-company-microservices"
environment          = "dev"
```

## Outputs for GitHub Secrets

After running `terraform apply`, add these to GitHub Secrets:

- `ECR_USER_SERVICE_REPOSITORY_URL` - From `user_service_repository_url` output
- `ECR_ORDER_SERVICE_REPOSITORY_URL` - From `order_service_repository_url` output
- `ECR_REGISTRY_URL` - From `ecr_registry_url` output
