import threading
import time
import random
import logging
from pydantic import BaseModel
import requests

logger = logging.getLogger("firewall.traffic_capture")

class TrafficData(BaseModel):
    source_ip: str
    dest_ip: str
    protocol: str
    bytes_sent: int
    bytes_recv: int
    duration: float
    flags: str

def simulate_zeek_capture():
    protocols = ["TCP", "UDP", "ICMP"]
    flags_list = ["SYN", "ACK", "SYN,ACK", "FIN", "RST"]
    ips = ["192.168.1.100", "10.0.0.5", "172.16.0.4", "8.8.8.8", "1.1.1.1"]
    
    while True:
        data = {
            "source_ip": random.choice(ips),
            "dest_ip": random.choice(ips),
            "protocol": random.choice(protocols),
            "bytes_sent": random.randint(100, 5000),
            "bytes_recv": random.randint(100, 5000),
            "duration": random.uniform(0.1, 5.0),
            "flags": random.choice(flags_list)
        }
        time.sleep(2)

def start_capture():
    t = threading.Thread(target=simulate_zeek_capture, daemon=True)
    t.start()
    logger.info("Zeek traffic capture simulation started.")
