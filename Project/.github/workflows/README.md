# GitHub Actions Workflows

This directory contains CI/CD workflows for the DevOps project.

## Workflows

### 1. CI Workflow (`ci.yml`)
**Trigger:** Push/PR to `main` or `develop` branches  
**Jobs:** test, lint, docker-build

### 2. CD Workflow (`cd.yml`)
**Trigger:** Push to `main`, or tags `v*`  
**Jobs:** build-and-push (ECR), build-local-test (non-main/manual)

### 3. Manual Workflow (`workflow_dispatch.yml`)
**Trigger:** Manual dispatch from GitHub Actions UI  
**Options:** choose environment, toggle tests/build

## Setup (CD)
1. Create ECR repo `user-microservice` (or update `ECR_REPOSITORY`).
2. Add GitHub Secrets: `AWS_ROLE_ARN` (recommended) or `AWS_ACCESS_KEY_ID` + `AWS_SECRET_ACCESS_KEY`.
3. Update `AWS_REGION` in `cd.yml` if needed.

## Badges (add to README)
```
![CI](https://github.com/your-username/your-repo/actions/workflows/ci.yml/badge.svg)
![CD](https://github.com/your-username/your-repo/actions/workflows/cd.yml/badge.svg)
```

## Troubleshooting
- Workflows not triggering: check branch names and YAML syntax.
- CI failing: run `python test_app.py` locally.
- CD failing: verify AWS creds, ECR repo exists, region matches.

## Status
✅ CI configured  
✅ CD configured (needs AWS secrets)  
✅ Manual dispatch available
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