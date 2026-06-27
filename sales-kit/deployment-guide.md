# Sovereign CRM — Demo Deployment Guide

## Quick Start (Local Demo)

### Prerequisites
- Docker Desktop (Windows/Mac) or Docker Compose (Linux)
- Git
- 2GB free RAM

### Steps
```bash
git clone https://github.com/sovereign-crm/sovereign
cd sovereign
docker compose up
```

Open http://localhost:3000

### Demo Credentials
| Role | Email | Password |
|------|-------|----------|
| Admin | admin@sovereign.local | admin1234 |
| Sales Manager | sarah@acme.local | (set during setup) |
| Sales Rep | marcus@acme.local | (set during setup) |

### Sample Data
The demo comes pre-loaded with:
- 50 contacts across 7 organizations
- 20 leads at various stages (New through Won/Lost)
- 10 deals across the pipeline
- 7 pipeline stages with probabilities

## Sharing the Demo Externally

### Option 1: ngrok (Recommended for Calls)
```bash
# After docker compose up is running:
ngrok http 3000
```
This gives you a public URL like `https://abc123.ngrok.io` to share.

### Option 2: Deploy to a VPS
```bash
scp -r . user@your-server:/opt/sovereign
ssh user@your-server
cd /opt/sovereign
docker compose up -d
```
Configure nginx/Caddy for HTTPS.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Port 3000 already in use | Edit docker-compose.yml, change 3000:3000 to 3001:3000 |
| Docker not running on Windows | Start Docker Desktop, ensure WSL2 backend |
| Postgres connection refused | Run `docker compose down -v && docker compose up` |
| Seed data not loading | Run `docker compose exec api go run ./cmd/server/main.go -migrate` |
| pg_isready failing | Wait 15 seconds on first run (Postgres needs to initialize) |
