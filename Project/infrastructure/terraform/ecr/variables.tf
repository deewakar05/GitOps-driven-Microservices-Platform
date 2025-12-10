variable "aws_region" {
  description = "AWS region for ECR repositories"
  type        = string
  default     = "us-east-1"
}

variable "ecr_repository_prefix" {
  description = "Prefix for ECR repository names"
  type        = string
  default     = "microservices-platform"
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "dev"
}
