# AIChieftain: Hotel Concierge AI Chatbot 🏨

A next-generation AI-powered hotel chatbot and admin dashboard, developed for the IIT Hackathon 2025 (Challenge: AIChieftain). This innovative system leverages cutting-edge Large Language Model (LLM) technology to streamline hotel operations, handling everything from room bookings and service requests to FAQs and sentiment analysis.

---

## 🚀 Features

Our Hotel Concierge AI Chatbot is packed with features designed to enhance both guest experience and staff efficiency:

- **Voice and Text-Based Chatbot:** Guests can interact seamlessly using either voice commands or text input.  
- **Intelligent Booking System:** Real-time availability checks ensure accurate room bookings.  
- **Room Service Request Management:** Guests can request room services with immediate SMS confirmation.  
- **AI-Generated Replies:** Powered by Google Gemini, the chatbot delivers context-aware responses.  
- **Sentiment Analysis & Dashboard Summary:** AI-driven insights into guest sentiment, visualized in a user-friendly dashboard.  
- **Comprehensive Admin Panel:** A dedicated interface for staff to manage bookings, requests, and sentiment data.

---

## 📄 Tech Stack

This project is built on a modern, scalable stack:

- **Frontend:** React (Chatbot UI & Admin Dashboard)  
- **Backend:** FastAPI (Python)  
- **LLM:** Gemini 1.5 Flash (via LangChain)  
- **Database:** Supabase  
- **Email Service:** SendGrid  
- **SMS Service:** Twilio  

---

## 🌐 Live Demo

Try it out in your browser:

- **Chatbot:** `https://chief-train-hr5t.vercel.app`  
- **Admin Panel:** `https://chief-train-hr5t.vercel.app/admin`  

---

## 🔧 Setup Instructions

Follow these steps to run the project locally:

1. **Clone the repository**  
   ```bash
   git clone ChiefTain
   cd ChiefTain

2. **Create a .env file in the  ChiefTain/backend with the following variables:**  
   ```bash
   SUPABASE_URL=…
   SUPABASE_KEY=…
   GEMINI_API_KEY=…
   SENDGRID_API_KEY=…
   TWILIO_ACCOUNT_SID=…
   TWILIO_AUTH_TOKEN=…
   TWILIO_PHONE_NUMBER=…


3. **Start the backend (FastAPI):**  
   ```bash
   cd backend
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload


4. **Start the frontend (React):**  
   ```bash
   cd frontend
   npm install
   npm run dev


## 🌐 Sample user
   To explore the system's functionalities, you can use these sample user profiles:
    -**Room Guest**: Access the chatbot to make queries, book rooms, or request services.
    -**Admin**: Log in to the admin panel with the password hotel@123 to manage backend operations, requests, and bookings.

 
