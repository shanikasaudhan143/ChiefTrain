from fastapi import APIRouter
from app.schemas import ChatRequest
from app.supabase_client import supabase
from langchain.llms import OpenAI
import os
router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)

llm = OpenAI(model_name="gpt-3.5-turbo",
        temperature=0.7,
        openai_api_key=os.getenv("OPENAI_API_KEY"))

@router.post("/")
async def chat(req: ChatRequest):
    prompt = f"""
You are the AI Concierge of The Grand Palace Hotel.
Your job is to help guests by answering questions about the hotel, amenities, booking, and policies.

Hotel Information:
- Check-in time: 2 PM
- Check-out time: 11 AM
- Breakfast: Complimentary buffet from 7 AM to 10 AM
- Wi-Fi: Free in all rooms and public areas
- Pool hours: 8 AM to 8 PM
- Pet policy: Pets are not allowed.

When you respond, be polite, warm, and professional.
If the question is not related to the hotel, respond: "I am only able to help you with hotel-related queries."

Guest question: {req.message}

Provide your response:
"""
    response = llm.predict(prompt)

    supabase.table("chats").insert({
        "user_id": req.user_id,
        "message": req.message,
        "response": response
    }).execute()

    return {"response": response}

# NEW ENDPOINT for Sentiment
@router.post("/sentiment")
async def sentiment(req: ChatRequest):
    prompt = f"""
Classify the sentiment of this message as Positive, Neutral, or Negative.

Message: {req.message}

Sentiment:
"""
    sentiment = llm.predict(prompt).strip()

    return {"sentiment": sentiment}
