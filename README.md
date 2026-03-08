# AI-Driven Next-Generation Firewall

A complete, production-ready implementation of a Next-Generation Firewall with AI-driven dynamic threat detection and Zero Trust implementation.

## Features
- **Backend:** FastAPI + Scikit-Learn/TensorFlow
- **ML Models:** LSTM (anomaly detection) + Isolation Forest (zero-day threats)
- **Frontend:** React + TailwindCSS real-time dashboard
- **Network:** Dynamic policy generation for `nftables`
- **Zero Trust:** Continuous device posture verification
- **Infrastructure:** Docker Compose (PostgreSQL, Redis, Nginx)

## Quick Start
1. **Run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

2. **Access the Application:**
   - **Dashboard:** `http://localhost` (proxied via Nginx)
   - **API Docs:** `http://localhost:8000/docs`

## Architecture overview
- `backend/threat_engine.py`: Orchestrates LSTM and Isolation Forest to score incoming traffic.
- `backend/dynamic_policy.py`: Auto-generates `nftables` commands to block/quarantine malicious IPs.
- `backend/zero_trust.py`: Verifies endpoints continuously before allowing standard traffic flows.
- `frontend/src/App.jsx`: Visualizes traffic and threats in real-time.
