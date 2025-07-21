from fastapi import APIRouter
from pydantic import BaseModel
from app.supabase_client import supabase
from app.sms_utils import send_sms  # ➕ Import the SMS function

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
    # Ensure phone number starts with +91
    phone_number = req.phone_number.strip()
    if not phone_number.startswith("+91"):
        if phone_number.startswith("0"):
            phone_number = "+91" + phone_number[1:]
        elif phone_number.startswith("91"):
            phone_number = "+" + phone_number
        else:
            phone_number = "+91" + phone_number

    # Save to Supabase
    record = supabase.table("room_requests").insert({
        "room_number": req.room_number,
        "phone_number": phone_number,
        "request": req.request,
        "status": "pending"
    }).execute()

    # Send SMS to guest
    message = (
        f"📩 Dear Guest in Room {req.room_number},\n"
        f"Your request \"{req.request}\" has been received. We’ll update you once it’s resolved."
    )
    send_sms(to=phone_number, body=message)

    return {"message": "Request logged and SMS sent"}


@router.get("/")
async def get_requests():
    data = supabase.table("room_requests").select("*").order("created_at").execute()
    return {"requests": data.data}

@router.patch("/{request_id}/resolve")
async def mark_resolved(request_id: str):
    # Fetch request to get phone number and info
    data = supabase.table("room_requests") \
        .select("*") \
        .eq("id", request_id) \
        .single() \
        .execute()
    request_data = data.data

    # Update status in DB
    supabase.table("room_requests") \
        .update({"status": "resolved"}) \
        .eq("id", request_id) \
        .execute()

    # Normalize phone number for India
    raw_phone = request_data["phone_number"].strip()
    if not raw_phone.startswith("+91"):
        normalized_phone = "+91" + raw_phone.lstrip("0")  # strip any leading zeroes
    else:
        normalized_phone = raw_phone

    # Send resolution SMS
    message = (
        f"✅ Hello! Your request “{request_data['request']}” "
        f"for Room {request_data['room_number']} has been resolved. Thank you!"
    )
    send_sms(to=normalized_phone, body=message)

    return {"message": "Request marked as resolved and SMS sent"}



@router.delete("/{request_id}")
async def delete_request(request_id: str):
    print("Deleting request with ID:", request_id)
    supabase.table("room_requests").delete().eq("id", request_id).execute()
    return {"message": "Request deleted"}
