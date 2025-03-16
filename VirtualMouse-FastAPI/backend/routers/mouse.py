from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from services.mouse_service import mouse_service

router = APIRouter()

@router.get("/video_feed")
async def video_feed():
    return StreamingResponse(mouse_service.generate_frames(),
                            media_type="multipart/x-mixed-replace; boundary=frame")

@router.post("/toggle_virtual_mouse")
async def toggle_virtual_mouse():
    enabled = mouse_service.toggle_virtual_mouse()
    return {"status": "success", "enabled": enabled}