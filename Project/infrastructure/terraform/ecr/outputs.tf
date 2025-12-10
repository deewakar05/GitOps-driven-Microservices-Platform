output "user_service_repository_url" {
  description = "URL of the user-service ECR repository"
  value       = aws_ecr_repository.user_service.repository_url
}

output "order_service_repository_url" {
  description = "URL of the order-service ECR repository"
  value       = aws_ecr_repository.order_service.repository_url
}

output "user_service_repository_name" {
  description = "Name of the user-service ECR repository"
  value       = aws_ecr_repository.user_service.name
}

output "order_service_repository_name" {
  description = "Name of the order-service ECR repository"
  value       = aws_ecr_repository.order_service.name
}

data "aws_caller_identity" "current" {}

output "ecr_registry_url" {
  description = "ECR registry URL"
  value       = "${data.aws_caller_identity.current.account_id}.dkr.ecr.${var.aws_region}.amazonaws.com"
}
