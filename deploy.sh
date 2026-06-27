#!/bin/bash
# Revenue OS — Deploy to Railway Free Tier
#
# Prerequisites:
#   1. Railway CLI: npm install -g @railway/cli
#   2. Railway account: https://railway.app
#   3. API key: railway login
#
# Usage:
#   chmod +x deploy.sh
#   ./deploy.sh

set -e

echo "=========================================="
echo "  Revenue OS — Deploy to Railway"
echo "=========================================="

# Check prerequisites
if ! command -v railway &> /dev/null; then
    echo "Installing Railway CLI..."
    npm install -g @railway/cli
fi

# Check for API key
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cat > .env << 'EOF'
OPENROUTER_API_KEY=
ANTHROPIC_API_KEY=
API_KEY=revenue-os-prod-2026
ENVIRONMENT=production
LOG_LEVEL=INFO
PORT=8080
EOF
    echo "⚠️  Edit .env with your API keys before deploying"
    echo "   OPENROUTER_API_KEY: Free key at https://openrouter.ai/keys"
    echo "   API_KEY: Set a secure random key for API authentication"
    exit 1
fi

# Check Railway login
echo "Checking Railway login..."
railway whoami 2>/dev/null || railway login

# Link or init project
if [ ! -f railway.json ]; then
    echo "Creating railway.json..."
    cat > railway.json << 'EOF'
{
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "Dockerfile"
  },
  "deploy": {
    "startCommand": "",
    "healthcheckPath": "/health",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
EOF
fi

# Deploy
echo "=========================================="
echo "  Deploying to Railway..."
echo "=========================================="
railway up --detach

echo ""
echo "✅ Deployed! Run 'railway status' to check."
echo "   Your URL will be shown by: railway domain"
echo ""
echo "To configure WhatsApp webhook:"
echo "   POST https://your-app.railway.app/webhook/twilio"
echo "   Header: X-API-Key: your-api-key"
