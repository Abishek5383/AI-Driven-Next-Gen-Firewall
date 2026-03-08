import jwt
from datetime import datetime, timedelta
import logging

logger = logging.getLogger("firewall.zero_trust")

SECRET_KEY = "SUPER_SECRET_ZERO_TRUST_KEY"
ALGORITHM = "HS256"

_device_posture_db = {
    "192.168.1.100": {"is_compliant": True, "risk_score": 0.1, "last_verified": datetime.utcnow()},
    "10.0.0.5": {"is_compliant": False, "risk_score": 0.9, "last_verified": datetime.utcnow()},
}

def verify_device(ip_address: str) -> bool:
    posture = _device_posture_db.get(ip_address)
    
    if not posture:
        logger.warning(f"Zero Trust verification failed for unknown IP: {ip_address}")
        return False
        
    if not posture["is_compliant"] or posture["risk_score"] > 0.7:
        logger.warning(f"Device {ip_address} is non-compliant or high risk.")
        return False
        
    time_since_verify = (datetime.utcnow() - posture["last_verified"]).total_seconds()
    if time_since_verify > 3600:
        logger.warning(f"Device {ip_address} needs re-verification.")
        
    return True

def generate_mtls_token(device_id: str):
    payload = {
        "sub": device_id,
        "exp": datetime.utcnow() + timedelta(hours=1),
        "type": "mtls_auth"
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def validate_mtls_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except jwt.PyJWTError:
        return None
