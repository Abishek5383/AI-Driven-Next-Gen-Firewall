import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import os
import logging

logger = logging.getLogger("firewall.lstm")
MODEL_PATH = "lstm_anomaly_model.h5"

def build_lstm_model(input_shape):
    model = Sequential([
        LSTM(64, activation='relu', input_shape=input_shape, return_sequences=True),
        Dropout(0.2),
        LSTM(32, activation='relu'),
        Dropout(0.2),
        Dense(16, activation='relu'),
        Dense(input_shape[1]) 
    ])
    model.compile(optimizer='adam', loss='mse')
    return model

def train_lstm(X_train):
    logger.info("Training new LSTM model...")
    model = build_lstm_model((X_train.shape[1], X_train.shape[2]))
    # Dummy training for completeness
    model.fit(X_train, X_train, epochs=2, batch_size=32, validation_split=0.1, verbose=1)
    model.save(MODEL_PATH)
    logger.info("LSTM model saved.")
    return model

def load_or_train_lstm():
    if os.path.exists(MODEL_PATH):
        logger.info(f"Loading LSTM model from {MODEL_PATH}")
        return tf.keras.models.load_model(MODEL_PATH)
    else:
        dummy_X = np.random.rand(100, 10, 5) # 100 samples, 10 timesteps, 5 features
        return train_lstm(dummy_X)

def predict_anomaly(model, sequence):
    seq = np.array(sequence).reshape(1, len(sequence), -1)
    pred = model.predict(seq, verbose=0)
    mse = np.mean(np.power(seq - pred, 2))
    return float(mse)

# Lazy loading of model
_model = None
def get_lstm_model():
    global _model
    if _model is None:
        _model = load_or_train_lstm()
    return _model
