from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query, status

from app.websocket.manager import manager
from app.core.security import decode_token


router = APIRouter()


@router.websocket("/ws/notifications")
async def notifications_websocket(
    websocket: WebSocket,
    token: str = Query(...),
):
    try:
        payload = decode_token(token)
        user_id = int(payload.get("sub"))
    except Exception:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await manager.connect(user_id, websocket)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(user_id, websocket)
