# GHCR AUTHENTICATION FIX GUIDE

## Problem
GHCR.io returns 403 Forbidden when trying to pull images:
  Error: unable to copy from source docker://ghcr.io/[repo]: initializing source docker://ghcr.io/[repo]: Requesting bearer token: received unexpected HTTP status: 403 Forbidden

## Solutions

### Option 1: Authenticate with GHCR (Recommended if you have GitHub access)
1. Generate a GitHub Personal Access Token with `read:packages` scope
2. Login to GHCR:
   ```bash
   podman login ghcr.io
   # Username: your GitHub username
   # Password: your personal access token
   ```
3. Retry pulling images:
   ```bash
   podman pull ghcr.io/langgenius/dify-api:latest
   podman pull ghcr.io/langgenius/dify-web:latest
   podman pull ghcr.io/triggerdotdev/trigger.dev:latest
   ```

### Option 2: Use Docker Hub Mirrors (Works without GHCR auth)
Some images are also available on Docker Hub:
- dify-api: `docker.io/langgenius/dify-api:latest` ✓ WORKS
- dify-web: `docker.io/langgenius/dify-web:latest` ✓ WORKS  
- directus: `docker.io/directus/directus:latest` ✓ WORKS
- billionmail: Not available on Docker Hub (use alternative or self-build)
- trigger.dev: Not available on Docker Hub (requires GHCR)

### Option 3: Use Alternative Images
For unavailable images, consider:
- BillionMail: Use `usesend/useSend` (already installed) or self-hosted postal/Mailu
- Trigger.dev: Use `n8n-io/n8n` or `langflow-ai/langflow` for workflow automation

## Verification
After fixing auth, verify with:
```bash
podman ps -a --format "table {{.Names}}	{{.Status}}	{{.Image}}"
```

## Applied Fixes in this Session
- Tested Docker Hub: dify-api, dify-web, directus all available
- Deployed Directus, Dify API, Dify Web, Dify Worker using Docker Hub images
- Some containers may be running despite podman command timeouts (WSL proxy issue)
- PostgreSQL (5432), Valkey (6379), ClickHouse (9000) confirmed running
