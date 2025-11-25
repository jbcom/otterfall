#!/usr/bin/env python
"""
Webhook Proxy Server - Routes Meshy API webhooks to GitHub Actions

This server receives webhooks from Meshy API and triggers GitHub Actions
workflows via repository_dispatch events.

Run locally with ngrok for development:
    ngrok http 8000
    GITHUB_TOKEN=xxx python webhook_proxy.py

Or deploy to a cloud function (AWS Lambda, Cloud Functions, etc.)

Environment variables:
    GITHUB_TOKEN: Personal access token or GitHub App token with repo scope
    GITHUB_REPO: Repository in format "owner/repo"
    WEBHOOK_SECRET: Optional shared secret for webhook verification
"""

import os
import json
import hmac
import hashlib
from typing import Optional
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request
import urllib.error


# Configuration
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_REPO = os.environ.get("GITHUB_REPO")  # Required - must be set explicitly
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", "")
PORT = int(os.environ.get("PORT", 8000))


def verify_signature(payload: bytes, signature: str) -> bool:
    """Verify webhook signature if secret is configured.
    
    WARNING: If WEBHOOK_SECRET is not set, signature verification is bypassed.
    This allows any external party to trigger GitHub Actions workflows.
    Always set WEBHOOK_SECRET in production environments.
    """
    if not WEBHOOK_SECRET:
        import sys
        print("WARNING: WEBHOOK_SECRET not configured - signature verification disabled!", file=sys.stderr)
        print("WARNING: Any source can trigger workflows. Set WEBHOOK_SECRET in production.", file=sys.stderr)
        return True

    expected = hmac.new(
        WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(f"sha256={expected}", signature)


def trigger_github_dispatch(event_type: str, payload: dict) -> bool:
    """Trigger GitHub repository_dispatch event."""
    if not GITHUB_TOKEN:
        print("ERROR: GITHUB_TOKEN not set")
        return False

    url = f"https://api.github.com/repos/{GITHUB_REPO}/dispatches"

    data = json.dumps({
        "event_type": event_type,
        "client_payload": payload
    }).encode()

    request = urllib.request.Request(
        url,
        data=data,
        headers={
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Content-Type": "application/json",
            "X-GitHub-Api-Version": "2022-11-28"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(request) as response:
            print(f"GitHub dispatch triggered: {event_type} -> {response.status}")
            return response.status == 204
    except urllib.error.HTTPError as e:
        print(f"GitHub dispatch failed: {e.code} {e.reason}")
        print(e.read().decode())
        return False


class WebhookHandler(BaseHTTPRequestHandler):
    """Handle incoming Meshy webhooks."""

    def do_POST(self):
        """Process POST webhook from Meshy API."""
        # Read body
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        # Verify signature if configured
        signature = self.headers.get("X-Webhook-Signature", "")
        if not verify_signature(body, signature):
            self.send_error(401, "Invalid signature")
            return

        # Parse JSON payload
        try:
            data = json.loads(body.decode())
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON")
            return

        # Extract info from path: /webhooks/meshy/{species}/{stage}
        path_parts = self.path.strip("/").split("/")
        if len(path_parts) < 4 or path_parts[0] != "webhooks" or path_parts[1] != "meshy":
            self.send_error(400, "Invalid path format")
            return

        species = path_parts[2]
        stage = path_parts[3]  # static, rigged, walk, attack, retextured

        # Map stage to GitHub event type
        event_type_map = {
            "static": "meshy_webhook_static",
            "rigged": "meshy_webhook_rigged",
            "walk": "meshy_webhook_animated",
            "attack": "meshy_webhook_animated",
            "idle": "meshy_webhook_animated",
            "retextured": "meshy_webhook_retextured",
        }

        event_type = event_type_map.get(stage, "meshy_webhook_unknown")

        # Build payload for GitHub
        github_payload = {
            "task_id": data.get("task_id") or data.get("result"),
            "status": data.get("status", "UNKNOWN"),
            "species": species,
            "stage": stage,
            "animation_type": stage if stage in ["walk", "attack", "idle"] else None,
            "spec_hash": data.get("spec_hash", ""),
            "model_url": data.get("model_url") or data.get("model_urls", {}).get("glb"),
            "raw_payload": data
        }

        print(f"Received webhook: {species}/{stage} -> {event_type}")
        print(f"Task ID: {github_payload['task_id']}, Status: {github_payload['status']}")

        # Trigger GitHub Action
        success = trigger_github_dispatch(event_type, github_payload)

        if success:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "dispatched"}).encode())
        else:
            self.send_error(500, "Failed to dispatch to GitHub")

    def do_GET(self):
        """Health check endpoint."""
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "healthy",
                "github_repo": GITHUB_REPO,
                "github_token_set": bool(GITHUB_TOKEN)
            }).encode())
        else:
            self.send_error(404)


def main():
    """Run webhook proxy server."""
    if not GITHUB_TOKEN:
        print("ERROR: GITHUB_TOKEN not set - dispatches will fail")
        
    if not GITHUB_REPO:
        print("ERROR: GITHUB_REPO not set - must be in format 'owner/repo'")
        print("Set GITHUB_REPO environment variable before starting the server.")
        import sys
        sys.exit(1)

    print(f"Starting webhook proxy on port {PORT}")
    print(f"GitHub repo: {GITHUB_REPO}")
    print(f"Webhook secret: {'configured' if WEBHOOK_SECRET else 'NOT CONFIGURED (insecure!)'}")

    server = HTTPServer(("0.0.0.0", PORT), WebhookHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
