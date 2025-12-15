# Automated CI/CD for a Dockerized Node.js App

Minimal Express app with GitHub Actions that tests, builds, and pushes a Docker image to Docker Hub.

## App
- `GET /` returns a JSON message: `Hello, DevOps! CI/CD Pipeline Working Successfully`.
- Code lives in `src/`, tests in `__tests__/`.

## Run locally
```bash
npm install
npm start      # http://localhost:3000
```

## Test
```bash
npm test
```

## Docker
```bash
docker build -t ci-cd-pipeline .
docker run -p 3000:3000 ci-cd-pipeline
```

### Verify locally
```bash
# In another terminal after the container is running
curl http://localhost:3000
# Expect: {"message":"Hello, DevOps! CI/CD Pipeline Working Successfully"}

# When finished, stop the container
docker ps --filter "name=ci-cd-pipeline"
docker stop ci-cd-pipeline
```

## CI/CD (GitHub Actions)
Workflow: `.github/workflows/ci.yml`
- Triggers on push/PR to `main`/`master` (or manual).
- Steps: install deps → run tests → build Docker image → push to Docker Hub when secrets are set.

### Required GitHub secrets for pushing
- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN` (Docker Hub access token or password)

Image tag used in CI: `${DOCKERHUB_USERNAME}/ci-cd-pipeline` with `:latest` and `:${GITHUB_SHA}`.

## Optional: Automated deploy to your server (SSH)
The workflow includes a `deploy` job that runs after image push when these secrets exist:
- `DEPLOY_HOST` (e.g., `203.0.113.10`)
- `DEPLOY_USER` (SSH username)
- `DEPLOY_KEY` (private key for that user; use a single-line value)
- `DEPLOY_PORT` (optional, default 22)

Prereqs on the target host:
- Docker installed and the user can run it
- Port 8080 available (change in the script if needed)

What it does:
- SSH to the host, `docker pull ${DOCKERHUB_USERNAME}/ci-cd-pipeline:latest`
- Replace any existing container named `ci-cd-pipeline`
- Run container detached on port 8080 → 3000 with env vars set:
  - `APP_ENV=prod`
  - `NODE_ENV=production`

If you need different ports or env vars, adjust the run command in `.github/workflows/ci.yml`.

## Optional deployment ideas
- Run the container on a VM (e.g., EC2) or any container host (Render/Railway).
- Keep the same image name for smooth pulls: `docker run -d -p 80:3000 ${DOCKERHUB_USERNAME}/ci-cd-pipeline:latest`.

## Architecture (high-level)
```
Developer push/PR
      |
GitHub Actions (test → build → push image)
      |
Docker Hub (image registry)
      |
Deploy job (SSH) pulls image
      |
Target host: container runs app (port 8080 → 3000)
```
