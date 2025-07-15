from pydantic import BaseModel

class ChatRequest(BaseModel):
    user_id: str
    message: str

class BookingRequest(BaseModel):
    user_id: str
    name: str
    room_type: str
    check_in: str
    check_out: str
