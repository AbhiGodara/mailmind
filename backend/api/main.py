from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel
import os
import redis
from typing import List

from backend.db.database import engine, get_db, Base
from backend.db.models import EmailSummary
from fastapi.middleware.cors import CORSMiddleware

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="MailMind API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redis connection for approval queue
redis_client = redis.Redis.from_url(os.environ.get("REDIS_URL", "redis://localhost:6379/0"), decode_responses=True)

class ApprovalRequest(BaseModel):
    action_id: str
    decision: str # "approve" or "reject"

@app.get("/api/stats")
def get_stats(db: Session = Depends(get_db)):
    total_emails = db.query(EmailSummary).count()
    high_priority = db.query(EmailSummary).filter(EmailSummary.priority == "HIGH").count()
    return {
        "total_emails": total_emails,
        "high_priority": high_priority,
        "drafts_generated": 0 # Track drafts separately if needed
    }

@app.get("/api/emails")
def get_emails(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    emails = db.query(EmailSummary).order_by(EmailSummary.date.desc()).offset(skip).limit(limit).all()
    return emails

@app.get("/api/senders")
def get_senders(db: Session = Depends(get_db)):
    from sqlalchemy import func
    results = db.query(EmailSummary.sender, func.count(EmailSummary.id).label('count')).group_by(EmailSummary.sender).order_by(func.count(EmailSummary.id).desc()).limit(10).all()
    return [{"sender": r.sender, "count": r.count} for r in results]

@app.post("/api/approve")
def approve_action(req: ApprovalRequest):
    if req.decision not in ["approve", "reject"]:
        raise HTTPException(status_code=400, detail="Decision must be 'approve' or 'reject'")
    redis_client.set(f"approval:{req.action_id}", req.decision, ex=86400) # 1 day expiry
    return {"status": "success", "action_id": req.action_id, "decision": req.decision}
