from fastapi import WebSocket
import time

class ConnectionStore:
    def __init__(self):
        self.connections: dict[str, set[WebSocket]] = {}
        self.last_pong: dict[str, dict[WebSocket, float]] = {}

    async def add(self, public_id: str, websocket: WebSocket):
        if public_id not in self.connections:
            self.connections[public_id] = set()
            self.last_pong[public_id] = {}

        self.connections[public_id].add(websocket)
        self.last_pong[public_id][websocket] = time.time()

    async def remove(self, public_id: str, websocket: WebSocket):
        if public_id in self.connections:
            self.connections[public_id].discard(websocket)
            self.last_pong[public_id].pop(websocket, None)

            if not self.connections[public_id]:
                self.connections.pop(public_id)
                self.last_pong.pop(public_id)

    async def get(self, public_id: str):
        return self.connections.get(public_id, set())

    async def broadcast(self, message: dict):
        for ws_set in self.connections.values():
            for ws in ws_set:
                await ws.send_json(message)

    def all_connections(self) -> list[tuple[str, WebSocket, float | None]]:
        result = []
        for public_id, ws_set in self.connections.items():
            for ws in ws_set:
                last = self.last_pong[public_id].get(ws)
                result.append((public_id, ws, last))
        return result

    def touch_pong(self, public_id: str, websocket: WebSocket) -> None:
        if public_id in self.last_pong:
            self.last_pong[public_id][websocket] = time.time()

connection_store = ConnectionStore()