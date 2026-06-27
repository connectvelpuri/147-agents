# SOVEREIGN CRM — DEPLOYMENT GUIDE

**Document Type:** Production Deployment Guide  
**Created:** 2026-06-07  
**Author:** Hermes Agent  
**Classification:** INTERNAL — NOT FOR GIT PUSH

---

## PREREQUISITES

### System Requirements
- **OS:** Ubuntu 22.04+ / Debian 12+ / RHEL 9+
- **CPU:** 2 cores minimum, 4 cores recommended
- **RAM:** 4GB minimum, 8GB recommended
- **Storage:** 20GB minimum, 50GB recommended
- **Network:** Public IP with DNS configured

### Software Requirements
- Podman 4+ (or Docker)
- Git
- OpenSSL (for SSL certificates)

---

## QUICK START (5 MINUTES)

### 1. Clone Repository
```bash
git clone https://github.com/sovereign-crm/sovereign.git
cd sovereign
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your settings
```

### 3. Start Services
```bash
sudo podman-compose -f podman-compose.prod.yml up -d
```

### 4. Access Application
- **Web:** https://your-domain.com
- **API:** https://your-domain.com/api

---

## DETAILED DEPLOYMENT

### Step 1: Server Setup

#### Install Podman
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y podman podman-compose

# RHEL/CentOS
sudo dnf install -y podman podman-compose
```

#### Configure Firewall
```bash
# Allow HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Allow SSH (if not already)
sudo ufw allow 22/tcp

# Enable firewall
sudo ufw enable
```

### Step 2: Domain & SSL

#### Option A: Let's Encrypt (Recommended)
```bash
# Install Certbot
sudo apt install -y certbot

# Get certificate
sudo certbot certonly --standalone -d your-domain.com

# Certificates will be at:
# /etc/letsencrypt/live/your-domain.com/fullchain.pem
# /etc/letsencrypt/live/your-domain.com/privkey.pem
```

#### Option B: Self-Signed (Testing Only)
```bash
# Generate self-signed certificate
openssl req -x509 -nodes -days 365 -newkey rsa:2048   -keyout privkey.pem -out fullchain.pem
```

### Step 3: Environment Configuration

Create `.env` file:
```bash
# Database
POSTGRES_DB=sovereign
POSTGRES_USER=sovereign
POSTGRES_PASSWORD=<strong-password>

# Redis
REDIS_PASSWORD=<strong-password>

# JWT
JWT_SECRET=<random-64-char-string>
JWT_REFRESH_SECRET=<random-64-char-string>

# Application
APP_URL=https://your-domain.com
API_URL=https://your-domain.com/api

# Email (optional)
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=your@email.com
SMTP_PASSWORD=<email-password>
```

### Step 4: Deploy with Podman

```bash
# Build and start all services
sudo podman-compose -f podman-compose.prod.yml up -d --build

# Check status
sudo podman-compose -f podman-compose.prod.yml ps

# View logs
sudo podman-compose -f podman-compose.prod.yml logs -f
```

### Step 5: Database Initialization

```bash
# Run migrations
sudo podman-compose -f podman-compose.prod.yml exec api   ./main migrate

# Seed demo data (optional)
sudo podman-compose -f podman-compose.prod.yml exec api   ./main seed
```

### Step 6: Verify Deployment

```bash
# Check health endpoint
curl https://your-domain.com/api/health

# Expected response:
# {"status":"healthy","version":"1.0.0"}
```

---

## PRODUCTION CONFIGURATION

### PostgreSQL Tuning
```sql
-- /etc/postgresql/16/main/postgresql.conf

# Memory
shared_buffers = 2GB
effective_cache_size = 6GB
work_mem = 64MB
maintenance_work_mem = 512MB

# Connections
max_connections = 200

# WAL
wal_buffers = 64MB
checkpoint_completion_target = 0.9

# Query Planning
random_page_cost = 1.1
effective_io_concurrency = 200
```

### Redis Tuning
```conf
# /etc/redis/redis.conf

# Memory
maxmemory 1gb
maxmemory-policy allkeys-lru

# Persistence
save 900 1
save 300 10
save 60 10000

# Security
requirepass <strong-password>
```

### API Configuration
```yaml
# Environment variables
GIN_MODE=release
LOG_LEVEL=info
CORS_ORIGINS=https://your-domain.com
RATE_LIMIT=100
```

---

## MONITORING & ALERTING

### Health Checks
```bash
# API health
curl https://your-domain.com/api/health

# PostgreSQL
sudo podman-compose -f podman-compose.prod.yml exec postgres   pg_isready

# Redis
sudo podman-compose -f podman-compose.prod.yml exec redis   redis-cli ping
```

### Log Management
```bash
# View API logs
sudo podman-compose -f podman-compose.prod.yml logs -f api

# View all logs
sudo podman-compose -f podman-compose.prod.yml logs -f

# Export logs
sudo podman-compose -f podman-compose.prod.yml logs > /var/log/sovereign.log
```

### Prometheus Metrics (Optional)
```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'sovereign-api'
    static_configs:
      - targets: ['api:8080']
    metrics_path: /metrics
```

---

## BACKUP & RESTORE

### Automated Backups
```bash
# /etc/cron.d/sovereign-backup
0 2 * * * root /opt/sovereign/scripts/backup.sh
```

### Backup Script
```bash
#!/bin/bash
# /opt/sovereign/scripts/backup.sh

BACKUP_DIR=/var/backups/sovereign
DATE=$(date +%Y%m%d_%H%M%S)

# Backup PostgreSQL
sudo podman-compose -f podman-compose.prod.yml exec -T postgres   pg_dump -U sovereign sovereign | gzip > $BACKUP_DIR/db_$DATE.sql.gz

# Backup Redis
sudo podman-compose -f podman-compose.prod.yml exec -T redis   redis-cli BGSAVE
sudo cp /data/dump.rdb $BACKUP_DIR/redis_$DATE.rdb

# Backup uploads
sudo tar -czf $BACKUP_DIR/uploads_$DATE.tar.gz /var/lib/sovereign/uploads

# Cleanup old backups (keep 30 days)
find $BACKUP_DIR -name "*.gz" -mtime +30 -delete
find $BACKUP_DIR -name "*.rdb" -mtime +30 -delete
```

### Restore from Backup
```bash
# Restore PostgreSQL
gunzip -c /var/backups/sovereign/db_20260607_020000.sql.gz |   sudo podman-compose -f podman-compose.prod.yml exec -T postgres   psql -U sovereign sovereign

# Restore Redis
sudo cp /var/backups/sovereign/redis_20260607_020000.rdb /data/dump.rdb
sudo podman-compose -f podman-compose.prod.yml restart redis
```

---

## TROUBLESHOOTING

### Common Issues

**Issue: Container won't start**
```bash
# Check logs
sudo podman-compose -f podman-compose.prod.yml logs api

# Check resource limits
sudo podman stats

# Restart services
sudo podman-compose -f podman-compose.prod.yml restart
```

**Issue: Database connection refused**
```bash
# Check PostgreSQL is running
sudo podman-compose -f podman-compose.prod.yml ps postgres

# Check connection
sudo podman-compose -f podman-compose.prod.yml exec postgres   psql -U sovereign -d sovereign -c "SELECT 1;"
```

**Issue: SSL certificate errors**
```bash
# Renew Let's Encrypt certificate
sudo certbot renew

# Restart Caddy
sudo podman-compose -f podman-compose.prod.yml restart caddy
```

**Issue: High memory usage**
```bash
# Check container stats
sudo podman stats

# Restart heavy containers
sudo podman-compose -f podman-compose.prod.yml restart api
```

---

## SECURITY HARDENING

### Container Security
```yaml
# Add to podman-compose.prod.yml
services:
  api:
    security_opt:
      - no-new-privileges:true
    read_only: true
    tmpfs:
      - /tmp
```

### Network Security
```bash
# Create isolated network
sudo podman network create sovereign-internal

# Restrict container communication
sudo podman-compose -f podman-compose.prod.yml   --network sovereign-internal up -d
```

### Log Rotation
```json
// /etc/docker/daemon.json (Docker) or podman config
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

---

*Document maintained by Hermes Agent. Never push to Git.*  
*Last Updated: 2026-06-07*
