# DevOps Project Report

**Project Title:** GitOps-driven Microservices Platform with Full Observability

**Student:** Deewakar Kumar

**Department:** Computer Science and Engineering

**Duration:** November–December 2025

---

## 1. Problem Statement

In modern software development, companies deploy hundreds of microservices that must be updated frequently and reliably. Traditional manual deployment approaches are slow, error-prone, and difficult to monitor. The lack of automation and observability often leads to deployment failures, untraceable bugs, and difficulty ensuring consistent environments. This project focuses on designing a fully automated DevOps workflow for microservices using industry-grade tools and practices.

## 2. Objective

The objective of this project is to design and implement an automated microservices deployment system that builds, tests, and deploys applications using GitOps principles, Terraform for infrastructure management, and observability tools like Prometheus, Grafana, and ECK.

## 3. Scope of the Project

The project demonstrates an end-to-end DevOps pipeline integrating GitHub Actions, Docker, AWS ECR, Terraform, ArgoCD, Prometheus, and ECK. It showcases a complete cloud-native deployment cycle with monitoring, logging, and automated rollbacks.

## 4. System Architecture

1. Developer commits code to GitHub.
2. GitHub Actions runs tests, builds Docker images, and pushes to AWS ECR.
3. Terraform provisions AWS EKS infrastructure.
4. ArgoCD watches a GitOps repo and deploys changes automatically.
5. Prometheus, Grafana, and ECK monitor and visualize metrics and logs.

## 5. Technologies and Tools Used

| Category | Tool / Technology | Purpose |
|----------|------------------|---------|
| Version Control | Git, GitHub | Source code management |
| CI/CD | GitHub Actions | Build, test, and deployment automation |
| Containerization | Docker | Consistent runtime environment |
| Registry | AWS ECR | Image storage |
| IaC | Terraform | Infrastructure provisioning |
| Orchestration | Kubernetes (EKS) | Container management |
| GitOps | ArgoCD | Version-controlled deployment |
| Monitoring | Prometheus, Grafana | Performance and metrics tracking |
| Logging | ECK (Elastic, Kibana) | Centralized log collection |

## 6. Implementation Plan

| Phase | Task | Outcome |
|-------|------|---------|
| Phase 1 | Build sample microservices | Working containerized app |
| Phase 2 | Setup CI pipeline with GitHub Actions | Automated build and testing |
| Phase 3 | Provision EKS using Terraform | Scalable cluster setup |
| Phase 4 | Implement GitOps with ArgoCD | Auto-deploy new versions |
| Phase 5 | Configure monitoring tools | Real-time performance insights |
| Phase 6 | Setup ECK logging | Centralized log management |
| Phase 7 | Testing and documentation | Ready-to-deploy project |

## 7. Expected Outcomes

- A fully automated CI/CD pipeline.
- End-to-end observability (metrics, alerts, logs).
- Version-controlled deployments with GitOps.
- Terraform-based infrastructure automation.
- Scalable and auditable cloud deployment.

## 8. Conclusion

This project implements a complete, production-grade DevOps workflow integrating CI/CD, IaC, GitOps, and observability. By automating the entire lifecycle from code to deployment and monitoring, it demonstrates how modern companies achieve reliability, scalability, and rapid delivery.

