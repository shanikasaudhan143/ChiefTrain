from fastapi import APIRouter
from app.schemas import BookingRequest
from app.supabase_client import supabase
from app.email_utils import send_booking_email

router = APIRouter(
    prefix="/booking",
    tags=["booking"]
)

@router.post("/")
async def create_booking(req: BookingRequest):
    # Check for existing booking with overlap
    existing = supabase.table("bookings").select("*").eq("room_type", req.room_type).eq("status", "confirmed").execute()
    conflict = False
    for b in existing.data:
        if not (
            req.check_out < b["check_in"] or req.check_in > b["check_out"]
        ):
            conflict = True
            break

    if conflict:
        return {"message": "Room not available for these dates."}

    confirmation = (
        f"Booking request for {req.name}, {req.room_type} room from "
        f"{req.check_in} to {req.check_out}."
    )
    supabase.table("bookings").insert({
        "user_id": req.user_id,
        "name": req.name,
        "room_type": req.room_type,
        "check_in": req.check_in,
        "check_out": req.check_out,
        "confirmation": confirmation,
        "status": "pending"
    }).execute()

    return {"message": "Booking request submitted! Await confirmation email."}


@router.get("/")
async def get_bookings():
    data = supabase.table("bookings").select("*").order("created_at").execute()
    return {"bookings": data.data}

@router.patch("/{booking_id}/status")
async def update_booking_status(booking_id: str, status: str):
    # Fetch booking to get email and info
    data = supabase.table("bookings").select("*").eq("id", booking_id).single().execute()
    booking = data.data

    if status == "confirmed":
        email_content = f"""
        <p>Dear {booking['name']},</p>
        <p>Your booking has been confirmed!</p>
        <p><strong>Room:</strong> {booking['room_type']}<br>
        <strong>Dates:</strong> {booking['check_in']} to {booking['check_out']}</p>
        """
        send_booking_email(
            to_email=booking["user_id"],
            subject="Booking Confirmed",
            content=email_content
        )
    elif status == "rejected":
        email_content = f"""
        <p>Dear {booking['name']},</p>
        <p>Unfortunately, we do not have availability for the requested dates.</p>
        <p>Please consider booking different dates. We apologize for the inconvenience.</p>
        """
        send_booking_email(
            to_email=booking["user_id"],
            subject="Booking Not Available",
            content=email_content
        )

    supabase.table("bookings").update({"status": status}).eq("id", booking_id).execute()

    return {"message": f"Booking marked as {status}"}
