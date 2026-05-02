import json
import logging
from typing import List, Dict, Any

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

from backend.core.bracket import TournamentManager

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Facial Recognition Tournament Ecosystem")

# In-memory storage for the current tournament state
tournament_state = {
    "players": [],
    "fixtures": [],
    "status": "idle"
}

class PlayerList(BaseModel):
    players: List[str]

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.get("/")
async def root():
    return {"message": "Tournament API is running"}

@app.post("/tournament/initialize")
async def initialize_tournament(data: PlayerList):
    global tournament_state
    tm = TournamentManager(data.players)
    fixtures = tm.generate_single_elimination()

    tournament_state = {
        "players": data.players,
        "fixtures": fixtures,
        "status": "active"
    }

    # Notify all connected clients about the new tournament state
    await manager.broadcast(json.dumps({
        "event": "tournament_initialized",
        "data": tournament_state
    }))

    return tournament_state

@app.get("/tournament/state")
async def get_tournament_state():
    return tournament_state

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        # Send initial state on connection
        await websocket.send_text(json.dumps({
            "event": "initial_state",
            "data": tournament_state
        }))
        while True:
            data = await websocket.receive_text()
            # Handle incoming messages if needed
            logger.info(f"Received from websocket: {data}")

            # Example: Kiosk sends a 'spin' event when a player is recognized
            message = json.loads(data)
            if message.get("event") == "spin_request":
                tm = TournamentManager(tournament_state["players"])
                winner_slot = tm.spin_the_wheel(tournament_state["fixtures"])

                if winner_slot:
                    # Update local state: mark this fixture as 'active' or 'spun'
                    for f in tournament_state["fixtures"]:
                        if f["id"] == winner_slot["id"]:
                            f["status"] = "active"
                            break

                    await manager.broadcast(json.dumps({
                        "event": "spin_result",
                        "data": winner_slot
                    }))
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)
