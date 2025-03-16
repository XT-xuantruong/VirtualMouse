from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from fastapi import WebSocket
from services.mouse_service import mouse_service

router = APIRouter()

@router.websocket("/video_ws")
async def video_websocket(websocket: WebSocket):
    await websocket.accept()
    try:
        async for frame in mouse_service.generate_frames():
            await websocket.send_bytes(frame)
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket.close()

# @router.get("/video_feed")
# async def video_feed():
#     return StreamingResponse(mouse_service.generate_frames(),
#                             media_type="multipart/x-mixed-replace; boundary=frame")

@router.post("/toggle_virtual_mouse")
async def toggle_virtual_mouse():
    enabled = mouse_service.toggle_virtual_mouse()
    return {"status": "success", "enabled": enabled}