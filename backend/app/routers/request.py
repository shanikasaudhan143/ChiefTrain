from fastapi import APIRouter
from pydantic import BaseModel
from app.supabase_client import supabase

router = APIRouter(
    prefix="/request",
    tags=["requests"]
)

class RoomRequest(BaseModel):
    room_number: str
    phone_number: str
    request: str

@router.post("/")
async def create_request(req: RoomRequest):
    record = supabase.table("room_requests").insert({
        "room_number": req.room_number,
        "phone_number": req.phone_number,
        "request": req.request,
        "status": "pending"
    }).execute()
    return {"message": "Request logged successfully"}

@router.get("/")
async def get_requests():
    data = supabase.table("room_requests").select("*").order("created_at").execute()
    return {"requests": data.data}

@router.patch("/{request_id}/resolve")
async def mark_resolved(request_id: str):
    supabase.table("room_requests").update({"status": "resolved"}).eq("id", request_id).execute()
    return {"message": "Request marked as resolved"}
