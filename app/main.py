from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from pydantic import BaseModel
from app.models import Lead
from app.services import add_lead, welcome_and_upsell, handle_vip
from app.utils import verify_signature
import json, os

app = FastAPI(title="Black4Me Automation")

@app.post("/webhook/fourthwall")
async def fw_hook(request: Request, bg: BackgroundTasks):
    raw = await request.body()
    sig = request.headers.get("X-Fourthwall-Signature")
    if not verify_signature(raw, sig):
        raise HTTPException(status_code=401, detail="Invalid signature")
    data = json.loads(raw)
    if data.get("event") == "ORDER_PLACED":
        lead = add_lead(data)
        item = data["order"]["line_items"][0]
        if item["type"] == "digital":
            bg.add_task(welcome_and_upsell, lead, item.get("download_url", ""))
        if "vip" in lead.tags:
            bg.add_task(handle_vip, lead)
    return {"status": "ok"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
