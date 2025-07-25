from fastapi import APIRouter, HTTPException
from app.schemas import ChatRequest
from app.supabase_client import supabase
from langchain_google_genai import ChatGoogleGenerativeAI
import logging
import json
import re
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
memory_store = {}

# Initialize FastAPI router
router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)

# Gemini LLM setup
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.7
)

@router.get("/ping")
async def ping():
    return {"status": "ok"}


@router.post("/")
async def chat(req: ChatRequest):
    user_id = req.user_id or "guest"
    message = req.message

    if not message:
        raise HTTPException(status_code=400, detail="Message is required")

    # Get user's chat history
    context = memory_store.get(user_id, [])
    context.append({"user": message})

    # Construct prompt from history
    history_prompt = ""
    for turn in context:
        if "user" in turn:
            history_prompt += f"Guest: {turn['user']}\n"
        if "bot" in turn:
            history_prompt += f"Concierge: {turn['bot']}\n"

    full_prompt = f"""
You are the AI Concierge of The Grand Palace Hotel.

Your job is to help guests by answering questions about the hotel, amenities, booking, and policies — in **whichever language the guest uses**.

Hotel Information:
Check-in: 2 PM

Check-out: 11 AM

Early check-in: Available upon request (subject to availability; extra fee may apply)

Late check-out: Available until 1 PM upon request (subject to availability; extra fee may apply)

Breakfast: Complimentary buffet from 7 AM to 10 AM

lunch: On-site restaurant open 11 AM to 2 PM

Dinner: On-site restaurant open 6 PM to 10 PM

On-site restaurant: Open 11 AM to 10 PM

24-Hour room service: Full menu available anytime

Wi-Fi: Free high-speed internet in all rooms and public areas

Business center: Computers, printers & meeting rooms; open 24/7

Fitness center: Open 24 hours (key-card access)

Spa & sauna: Open 9 AM to 8 PM (treatments by appointment)

Pool hours: 8 AM to 8 PM; towel service provided

Parking: Self-parking $15/night; valet $25/night

Airport shuttle: Complimentary (reservation required at least 4 hours in advance)

Pet policy: Pets not allowed (service animals welcome with advance notice)

Smoking policy: Non-smoking property (designated outdoor smoking area available)

Children’s policy: Kids under 12 stay free with existing bedding

Cancellation policy: Free up to 24 hours before arrival; thereafter one night’s charge

Payment & deposit: All major credit cards accepted; one-night deposit at check-in

Accessibility: Wheelchair-accessible rooms, elevators, and public areas

Safety: Fire exits, emergency procedures & first-aid kits on each floor

Concierge services: 24/7 assistance with tours, dining reservations & transportation

Housekeeping: Daily service 9 AM-5 PM; turndown on request

Laundry & dry-cleaning: Same-day service if dropped off by 9 AM


Respond politely and professionally in the **same language as the guest's message**.

Guest question: {req.message}

Provide your response:
"""

    sentiment_prompt = f"""
Classify the sentiment of this message as Positive, Neutral, or Negative.

Message: {req.message}

Sentiment:
"""
    # Get LLM response
    response = llm.invoke(full_prompt)
    bot_reply = response.content.strip()
    sentiment_response = llm.invoke(sentiment_prompt)
    sentiment = sentiment_response.content.strip()
    # Save response in memory
    context.append({"bot": bot_reply})
    memory_store[user_id] = context
    
    # Log in Supabase
    supabase.table("chats").insert({
        "user_id": user_id,
        "message": message,
        "response": bot_reply,
        "sentiment": sentiment
    }).execute()
    
    return {"response": bot_reply}


# Optional: Keep sentiment analysis as-is
@router.post("/sentiment")
async def sentiment(req: ChatRequest):
    sentiment_prompt = f"""
Classify the sentiment of this message as Positive, Neutral, or Negative.

Message: {req.message}

Sentiment:
"""
    sentiment_response = llm.invoke(sentiment_prompt)
    sentiment_text = sentiment_response.content.strip()

    return {"sentiment": sentiment_text}


@router.get("/sentiment-summary-ai")
async def ai_generated_sentiment_summary():
    result = supabase.table("chats").select("message, sentiment").execute()
    chats = result.data or []

    sentiments = {"Positive": [], "Negative": [], "Neutral": []}
    for chat in chats:
        sentiment_raw = (chat.get("sentiment") or "").strip().lower()
        message = chat.get("message", "").strip()

        if "positive" in sentiment_raw and message:
            sentiments["Positive"].append(message)
        elif "negative" in sentiment_raw and message:
            sentiments["Negative"].append(message)
        elif "neutral" in sentiment_raw and message:
            sentiments["Neutral"].append(message)


    # Trim long input
    positive = sentiments["Positive"][:30]
    negative = sentiments["Negative"][:30]
    neutral = sentiments["Neutral"][:30]

    prompt = f"""
You are a hotel AI assistant. Review the guest messages below categorized by sentiment and return a JSON with:

- top_positive: Top 5 positive messages
- top_negative: Top 5 negative messages
- top_neutral: Top 5 neutral or unclear messages

Positive:
{json.dumps(positive, indent=2)}

Negative:
{json.dumps(negative, indent=2)}

Neutral:
{json.dumps(neutral, indent=2)}

Respond in *pure JSON only*. Do NOT include markdown, comments, or backticks. Example format:
{{
  "top_positive": ["..."],
  "top_negative": ["..."],
  "top_neutral": ["..."]
}}
"""

    try:
        llm_response = llm.invoke(prompt)
        raw_content = llm_response.content if hasattr(llm_response, "content") else str(llm_response)
        clean = re.sub(r"^```json|```$", "", raw_content.strip()).strip()
        summary_json = json.loads(clean)
        logger.info(f"🎯 AI Sentiment Summary: {summary_json}")
    except Exception as e:
        logger.error(f"❌ JSON parsing failed: {e}")
        logger.error(f"Raw response: {llm_response}")
        summary_json = {
            "top_positive": [],
            "top_negative": [],
            "top_neutral": []
        }

    return summary_json