"""FastAPI webhook receiver for Meshy integration tests"""
import json
from pathlib import Path
from datetime import datetime
from fastapi import FastAPI, Request, Response
from pydantic import BaseModel

app = FastAPI()

webhook_storage_dir = Path(__file__).parent.parent / "cassettes" / "webhooks"
webhook_storage_dir.mkdir(parents=True, exist_ok=True)


class WebhookPayload(BaseModel):
    """Webhook payload storage"""
    task_id: str
    status: str
    progress: int
    task_type: str
    model_urls: dict | None = None
    error: dict | None = None
    received_at: str
    headers: dict


@app.post("/webhook/{species}/{task_type}")
async def receive_webhook(species: str, task_type: str, request: Request):
    """Receive webhook from Meshy and store payload"""
    body = await request.body()
    payload = json.loads(body)
    
    headers = dict(request.headers)
    
    webhook_data = WebhookPayload(
        task_id=payload.get("task_id", ""),
        status=payload.get("status", ""),
        progress=payload.get("progress", 0),
        task_type=payload.get("task_type", task_type),
        model_urls=payload.get("model_urls"),
        error=payload.get("error"),
        received_at=datetime.utcnow().isoformat(),
        headers=headers
    )
    
    storage_file = webhook_storage_dir / f"{species}_{task_type}_{webhook_data.task_id}.json"
    storage_file.write_text(webhook_data.model_dump_json(indent=2))
    
    print(f"[WEBHOOK] Received {task_type} webhook for {species}: {payload.get('status')}")
    print(f"[WEBHOOK] Stored at: {storage_file}")
    
    return Response(status_code=200)


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "ok"}
