import logging

logger = logging.getLogger("firewall.dynamic_policy")

def update_rules(ip_address: str, action: str, reason: str):
    logger.info(f"Updating policy: IP={ip_address}, Action={action}, Reason={reason}")
    
    if action.upper() == "BLOCK":
        logger.warning(f"[nftables] Added DROP rule for {ip_address}")
        
    elif action.upper() == "QUARANTINE":
        logger.warning(f"[nftables] Added QUARANTINE rule (redirect to honeypot) for {ip_address}")
