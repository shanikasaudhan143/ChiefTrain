import logging
from fastapi import APIRouter, Query
from app.schemas import BookingRequest
from app.supabase_client import supabase
from app.email_utils import send_booking_email
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/booking",
    tags=["booking"]
)

@router.post("/")
async def create_booking(req: BookingRequest):
    logger.info(f"🔹 Received booking request: {req.dict()}")
    
    existing = supabase.table("bookings").select("*").eq("room_type", req.room_type).eq("status", "confirmed").execute()
    logger.info(f"🔍 Existing confirmed bookings: {len(existing.data)}")

    conflict = False
    for b in existing.data:
        logger.debug(f"🗓️ Checking overlap with: {b}")
        if not (req.check_out < b["check_in"] or req.check_in > b["check_out"]):
            conflict = True
            logger.warning("⚠️ Booking conflict found.")
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

    logger.info("✅ Booking request inserted as 'pending'")
    return {"message": "Booking request submitted! Await confirmation email."}


@router.get("/")
async def get_bookings():
    data = supabase.table("bookings").select("*").order("created_at").execute()
    logger.info(f"📦 Returning {len(data.data)} bookings")
    return {"bookings": data.data}


@router.patch("/{booking_id}/status")
async def update_booking_status(booking_id: str, status: str):
    logger.info(f"🔄 Updating booking {booking_id} to status '{status}'")

    data = supabase.table("bookings").select("*").eq("id", booking_id).single().execute()
    booking = data.data

    if not booking:
        logger.error(f"❌ Booking ID {booking_id} not found")
        return {"message": "Booking not found"}

    if status == "confirmed":
        logger.info("📧 Sending confirmation email")
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
        logger.info("📧 Sending rejection email")
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
    logger.info(f"✅ Booking {booking_id} updated to '{status}'")

    return {"message": f"Booking marked as {status}"}


@router.get("/availability/")
def check_availability(check_in: str = Query(...), check_out: str = Query(...)):
    logger.info(f"📅 Checking availability from {check_in} to {check_out}")

    existing = supabase.table("bookings").select("*").eq("status", "confirmed").execute()
    logger.info(f"🔍 Fetched {len(existing.data)} confirmed bookings")

    room_counts = {"Deluxe": 10, "Suite": 20, "Standard": 30}

    user_check_in = datetime.strptime(check_in, "%Y-%m-%d").date()
    user_check_out = datetime.strptime(check_out, "%Y-%m-%d").date()

    for b in existing.data:
        b_check_in = datetime.strptime(b["check_in"], "%Y-%m-%d").date()
        b_check_out = datetime.strptime(b["check_out"], "%Y-%m-%d").date()

        logger.debug(f"🔄 Comparing with booking: {b}")
        logger.info(f"Comparing with booking: {b['room_type']} from {b['check_in']} to {b['check_out']}")
        logger.info(f"Parsed dates: {b_check_in} to {b_check_out}")
        logger.info(f"User wants from {user_check_in} to {user_check_out}")
        if not (user_check_out <= b_check_in or user_check_in > b_check_out):
            room_type = b["room_type"]
            if room_type in room_counts:
                room_counts[room_type] = max(0, room_counts[room_type] - 1)
                logger.info(f"➖ Decremented {room_type}: now {room_counts[room_type]}")

    logger.info(f"✅ Final room availability: {room_counts}")
    return room_counts

@router.delete("/{booking_id}")
async def delete_booking(booking_id: str):
    supabase.table("bookings").delete().eq("id", booking_id).execute()
    return {"message": "Booking deleted"}


