"""
Revenue OS API Server — Entry point for deployment.
Deploy to Railway: $0 free tier
"""

import os
import uvicorn

from api.webhook import app

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    host = os.getenv("HOST", "0.0.0.0")
    uvicorn.run(app, host=host, port=port)
