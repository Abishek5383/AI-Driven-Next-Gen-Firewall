from sklearn.ensemble import IsolationForest
import numpy as np
import joblib
import os
import logging

logger = logging.getLogger("firewall.iforest")
MODEL_PATH = "iforest_model.pkl"

def train_iforest(X_train):
    logger.info("Training new Isolation Forest model...")
    model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
    model.fit(X_train)
    joblib.dump(model, MODEL_PATH)
    logger.info("Isolation Forest model saved.")
    return model

def load_or_train_iforest():
    if os.path.exists(MODEL_PATH):
        logger.info(f"Loading Isolation Forest model from {MODEL_PATH}")
        return joblib.load(MODEL_PATH)
    else:
        dummy_X = np.random.rand(500, 5) # 5 features
        return train_iforest(dummy_X)

def predict_zero_day(model, features):
    feat = np.array(features).reshape(1, -1)
    pred = model.predict(feat) # -1 is anomaly, 1 is normal
    score = model.score_samples(feat) 
    return pred[0] == -1, -float(score[0]) # Return absolute anomaly score

_model = None
def get_iforest_model():
    global _model
    if _model is None:
        _model = load_or_train_iforest()
    return _model
