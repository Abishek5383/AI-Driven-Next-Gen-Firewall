from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import uvicorn
import redis
import json
import logging

from database import init_db, get_db, ThreatLog
from threat_engine import analyze_traffic
from zero_trust import verify_device
from dynamic_policy import update_rules
from traffic_capture import start_capture

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("firewall")

app = FastAPI(title="AI Next-Gen Firewall API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect to Redis for real-time alerts
try:
    redis_client = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)
except Exception as e:
    logger.error(f"Failed to connect to Redis: {e}")
    redis_client = None

class TrafficData(BaseModel):
    source_ip: str
    dest_ip: str
    protocol: str
    bytes_sent: int
    bytes_recv: int
    duration: float
    flags: str

@app.on_event("startup")
def on_startup():
    init_db()
    logger.info("Database initialized.")
    # Assuming start_capture() runs in a background thread
    start_capture()
    logger.info("Traffic capture started.")

@app.post("/api/analyze")
async def analyze_endpoint(data: TrafficData):
    # 1. Zero Trust Verification
    is_trusted = verify_device(data.source_ip)
    if not is_trusted:
        update_rules(data.source_ip, "BLOCK", "Failed zero trust verification")
        return {"status": "blocked", "reason": "Zero Trust Validation Failed"}
    
    # 2. AI Threat Analysis
    threat_score, threat_type = analyze_traffic(data.dict())
    
    if threat_score > 0.8: # Threshold for high alert
        update_rules(data.source_ip, "BLOCK", threat_type)
        if redis_client:
            redis_client.publish('threat_alerts', json.dumps({
                "ip": data.source_ip,
                "score": threat_score,
                "type": threat_type
            }))
        return {"status": "blocked", "score": threat_score, "type": threat_type}
        
    return {"status": "allowed", "score": threat_score}

@app.get("/api/threats")
def get_threats(db = Depends(get_db)):
    logs = db.query(ThreatLog).order_by(ThreatLog.timestamp.desc()).limit(10).all()
    return [{"id": l.id, "ip": l.source_ip, "type": l.threat_type, "score": l.anomaly_score, "action": l.action_taken} for l in logs]

@app.get("/api/stats")
def get_stats():
    return {
        "total_traffic_gb": 1.5,
        "active_threats": 2,
        "blocked_ips": 12,
        "system_health": 99.2
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
