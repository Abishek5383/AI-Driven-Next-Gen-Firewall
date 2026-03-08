import numpy as np
import logging
from models.lstm_model import get_lstm_model, predict_anomaly
from models.isolation_forest import get_iforest_model, predict_zero_day

logger = logging.getLogger("firewall.threat_engine")

def analyze_traffic(data_dict):
    features = extract_features(data_dict)
    
    # Isolation Forest for zero-day
    if_model = get_iforest_model()
    is_anomaly_if, if_score = predict_zero_day(if_model, features)
    
    # LSTM for anomaly scoring
    lstm_model = get_lstm_model()
    sequence = [features] * 10
    lstm_score = predict_anomaly(lstm_model, sequence)
    
    combined_score = (abs(if_score) + lstm_score) / 2.0
    threat_type = "Normal"
    if combined_score > 0.8:
        threat_type = "High Risk Anomaly"
    elif combined_score > 0.5:
        threat_type = "Suspicious Traffic"
        
    logger.info(f"Analyzed traffic from {data_dict.get('source_ip')}: score={combined_score:.4f}, type={threat_type}")
    return combined_score, threat_type

def extract_features(data_dict):
    proto_map = {"TCP": 1, "UDP": 2, "ICMP": 3}
    proto_val = proto_map.get(data_dict.get('protocol', 'TCP').upper(), 0)
    
    features = [
        proto_val,
        float(data_dict.get('bytes_sent', 0)) / 10000.0,
        float(data_dict.get('bytes_recv', 0)) / 10000.0,
        float(data_dict.get('duration', 0.1)),
        len(data_dict.get('flags', '')) / 10.0
    ]
    return features
