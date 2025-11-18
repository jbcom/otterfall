#!/usr/bin/env python3
"""Run FastAPI webhook receiver for Meshy callbacks"""

import sys
import uvicorn
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from tests.integration.webhook_server.app import app


def main():
    """Start webhook receiver on port 8000"""
    print("🌐 Starting Meshy webhook receiver...")
    print("   URL: http://localhost:8000")
    print("   Webhook endpoint: POST /webhook")
    print("\n⚠️  Don't forget to expose with ngrok:")
    print("   ngrok http 8000")
    print()
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")


if __name__ == "__main__":
    main()
