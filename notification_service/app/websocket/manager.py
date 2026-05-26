from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, list[WebSocket]] = {}

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()

        if user_id not in self.active_connections:
            self.active_connections[user_id] = []

        self.active_connections[user_id].append(websocket)

        print(f"WS CONNECTED user_id={user_id}")
        print(f"ACTIVE CONNECTIONS: {list(self.active_connections.keys())}")

    def disconnect(self, user_id: int, websocket: WebSocket):
        connections = self.active_connections.get(user_id)

        if not connections:
            return

        if websocket in connections:
            connections.remove(websocket)

        if not connections:
            self.active_connections.pop(user_id, None)

        print(f"WS DISCONNECTED user_id={user_id}")
        print(f"ACTIVE CONNECTIONS: {list(self.active_connections.keys())}")

    async def send_to_user(self, user_id: int, message: dict):
        connections = self.active_connections.get(user_id, [])

        print(f"WS SEND TO user_id={user_id}")
        print(f"CONNECTIONS FOUND: {len(connections)}")
        print(f"MESSAGE: {message}")

        for websocket in connections:
            await websocket.send_json(message)


manager = ConnectionManager()
