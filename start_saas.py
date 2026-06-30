"""DealForge SaaS - Railway entry point."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "agents"))

from web.saas_app import app

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
