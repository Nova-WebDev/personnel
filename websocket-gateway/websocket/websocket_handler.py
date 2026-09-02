from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from auth.jwt_decoder import JWTDecoder, JWTDecodeError
from websocket.connection_store import connection_store

router = APIRouter()
decoder = JWTDecoder()


@router.websocket("/ws")
async def websocket_handler(websocket: WebSocket):
    cookies = websocket.cookies or {}
    access_token = cookies.get("access_token")

    if access_token is None:
        await websocket.close(code=4401)
        return

    try:
        payload = decoder.decode(access_token)
    except JWTDecodeError:
        await websocket.close(code=4401)
        return

    public_id = payload.public_id

    await websocket.accept()
    await connection_store.add(public_id, websocket)

    try:
        while True:
            try:
                msg = await websocket.receive_text()
            except WebSocketDisconnect:
                break

            if msg == "pong":
                connection_store.touch_pong(public_id, websocket)

    finally:
        await connection_store.remove(public_id, websocket)