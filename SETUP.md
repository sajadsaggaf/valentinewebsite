# Setup Guide for ThinkPad P15v

This guide will help you get the Facial Recognition Tournament Ecosystem running locally on your laptop (Ubuntu/Linux) before deploying to the RDK X5.

## 1. Environment Setup

It is recommended to use a Python virtual environment.

```bash
# Create a virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## 2. Running the Backend

Start the FastAPI server using Uvicorn. Ensure you are in the **project root directory** (where `requirements.txt` is located).

```bash
# From the project root
export PYTHONPATH=$PYTHONPATH:.
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

> **Note**: If you get a `ModuleNotFoundError: No module named 'backend'`, ensure your current working directory contains the `backend/` folder and that you have added the current directory to your `PYTHONPATH` as shown above.

- **API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **WebSocket Endpoint**: `ws://localhost:8000/ws`

## 3. Initializing a Tournament

You can initialize a tournament via the API using `curl` or the `/docs` interface:

```bash
curl -X 'POST' \
  'http://localhost:8000/tournament/initialize' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "players": ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Heidi"]
}'
```

## 4. Testing Real-time Sync

To verify the "Spin the Wheel" logic and WebSocket broadcast, you can use the `mock_test_flow.py` script provided in the root directory.

```bash
python3 mock_test_flow.py
```

This script will:
1. Connect to the WebSocket.
2. Request a "Spin".
3. Listen for the broadcasted result.

## 5. Laptop Specifics (ThinkPad P15v)
Since you have a powerful NVIDIA RTX A2000, you could eventually run local inference using CUDA if you want to test face detection on the laptop. However, the current code is optimized for the RDK's BPU. For now, the backend logic runs purely on the CPU and is very lightweight.
