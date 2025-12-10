# Phase 2 Setup Guide (GitHub Actions + ECR)

## 1) Push code to GitHub
```bash
cd /Users/deewakarkumar/Devops/Project
git add .
git commit -m "Phase 2: CI/CD setup"
git push origin main
```

## 2) Configure GitHub Secrets
- `AWS_ROLE_ARN` (recommended) **or** `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`
- Optional: `AWS_REGION` override in workflow env

## 3) Create ECR repository
```bash
AWS_REGION=us-east-1
aws ecr create-repository \
  --repository-name user-microservice \
  --region $AWS_REGION \
  --image-scanning-configuration scanOnPush=true \
  --encryption-configuration encryptionType=AES256
```

## 4) Validate workflows
- CI: triggers on push/PR to `main` or `develop`
- CD: triggers on push to `main` or tags `v*`
- Manual: run from Actions UI (workflow_dispatch)

## 5) Troubleshooting
- Workflows not triggering: verify branch names and YAML indentation.
- CI failing: run `python test_app.py` locally.
- CD failing: check AWS creds, ECR repo, and region.

## Commands (local)
```bash
# Tests
cd microservice && python3 test_app.py

# Docker build
docker build -t user-microservice:local microservice
```
{
  "cells": [],
  "metadata": {
    "language_info": {
      "name": "python"
    }
  },
  "nbformat": 4,
  "nbformat_minor": 2
}