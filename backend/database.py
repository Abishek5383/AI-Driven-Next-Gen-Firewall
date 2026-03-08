import os
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/firewall")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ThreatLog(Base):
    __tablename__ = "threat_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    source_ip = Column(String, index=True)
    dest_ip = Column(String)
    threat_type = Column(String, index=True)
    anomaly_score = Column(Float)
    action_taken = Column(String) # blocked, alerted, quarantined
    mitre_tactic = Column(String)
    
class DevicePosture(Base):
    __tablename__ = "device_posture"
    
    device_id = Column(String, primary_key=True, index=True)
    last_verified = Column(DateTime, default=datetime.utcnow)
    is_compliant = Column(Boolean, default=True)
    os_version = Column(String)
    risk_score = Column(Float, default=0.0)

def init_db():
    Base.metadata.create_all(bind=engine)
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
