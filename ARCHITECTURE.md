# Facial Recognition Tournament Management Ecosystem

## Project Architecture

This project is divided into two main parts:

### 1. Kiosk (Local RDK X5) - `/kiosk`
Code running locally on the D-Robotics RDK X5 hardware.
- `hardware/`: Drivers and interface logic for USB/MIPI cameras and HDMI touchscreens.
- `capture/`: Face detection and recognition scripts (e.g., `enrollment.py`).
- **Optimization**: All face detection logic is designed to be offloaded to the RDK's BPU using `hobot_dnn`.

### 2. Backend (Cloud/Spectator) - `/backend`
Centralized FastAPI server for managing tournament state and serving real-time updates.
- `core/`: Business logic, including the Bracket Engine and "Spin the Wheel" generator (`bracket.py`).
- `api/`: REST endpoints for tournament management.
- `sockets/`: WebSocket logic for real-time sync with the kiosk and spectator frontend.
- `models/`: Data models for players, fixtures, and tournament state.

### 3. Frontend - `/frontend`
React/Vue.js application for spectators to view the bracket and "Spin the Wheel" animation in real-time.

---

## Getting Started

### Prerequisites
- Python 3.10+
- Linux environment (optimized for Ubuntu)

### Installation
```bash
pip install -r requirements.txt
```

### Running the Backend
```bash
uvicorn backend.main:app --reload
```
