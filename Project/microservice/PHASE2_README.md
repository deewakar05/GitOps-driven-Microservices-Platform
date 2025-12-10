# Phase 2: CI/CD Pipeline (GitHub Actions)

**Status:** Ready (requires repo + secrets)

## Overview
- CI: tests, lint, Docker build on push/PR to `main`/`develop`
- CD: build & push image to AWS ECR on push to `main` or tags `v*`
- Manual: workflow_dispatch with environment + options

## Files
- `.github/workflows/ci.yml`
- `.github/workflows/cd.yml`
- `.github/workflows/workflow_dispatch.yml`
- `.github/workflows/README.md`

## Setup
1) GitHub repo with Actions enabled  
2) AWS ECR repo (default: `user-microservice`, region `us-east-1`)  
3) GitHub Secrets:  
   - `AWS_ROLE_ARN` (recommended) OR `AWS_ACCESS_KEY_ID` + `AWS_SECRET_ACCESS_KEY`

## How it works
- CI: install deps → run tests → lint → build & test Docker image
- CD: assume role → login ECR → build → tag (SHA or version) → push
- Manual: optional tests + build for staging/production

## Test locally
```bash
cd microservice
python3 test_app.py
# docker build -t user-microservice:local .
```

## Next steps
- Add secrets in GitHub
- Push to trigger CI
- Push to `main` or tag `v*` to trigger CD
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