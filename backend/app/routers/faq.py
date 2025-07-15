from fastapi import APIRouter

router = APIRouter(
    prefix="/faq",
    tags=["faq"]
)

@router.get("/")
async def get_faq():
    faqs = [
        {"q": "What time is check-in?", "a": "Check-in is from 2 PM."},
        {"q": "Do you have Wi-Fi?", "a": "Yes, free Wi-Fi in all rooms."},
        {"q": "Can I cancel my booking?", "a": "Yes, up to 24 hours before arrival."},
    ]
    return {"faqs": faqs}
