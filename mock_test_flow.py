import asyncio
import websockets
import json
import requests
import time

BACKEND_URL = "http://localhost:8000"
WS_URL = "ws://localhost:8000/ws"

async def mock_kiosk_and_spectator():
    # 1. Initialize Tournament via REST
    print("--- 1. Initializing Tournament ---")
    players = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Heidi"]
    try:
        response = requests.post(f"{BACKEND_URL}/tournament/initialize", json={"players": players})
        print(f"Tournament Initialized: {response.status_code}")
    except Exception as e:
        print(f"Failed to connect to backend: {e}")
        return

    # 2. Connect to WebSocket (Spectator View)
    print("\n--- 2. Connecting to WebSocket (Spectator/Kiosk) ---")
    async with websockets.connect(WS_URL) as websocket:
        # Receive initial state
        msg = await websocket.recv()
        print(f"Received Initial State: {msg[:100]}...")

        # 3. Simulate Kiosk sending a Spin Request
        print("\n--- 3. Simulating Kiosk 'Spin Request' ---")
        spin_request = json.dumps({"event": "spin_request"})
        await websocket.send(spin_request)

        # 4. Listen for Broadcast Result
        while True:
            response_msg = await websocket.recv()
            data = json.loads(response_msg)
            if data["event"] == "spin_result":
                print("\n--- 4. SPIN RESULT RECEIVED! ---")
                print(json.dumps(data["data"], indent=2))
                break
            else:
                print(f"Received Event: {data['event']}")

if __name__ == "__main__":
    print("Note: Ensure the FastAPI server is running with 'uvicorn backend.main:app' before running this.")
    time.sleep(1)
    asyncio.run(mock_kiosk_and_spectator())
