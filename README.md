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

- **Chatbot:** `https://your-deployment-url/chatbot`  
- **Admin Panel:** `https://your-deployment-url/admin`  

---

## 🔧 Setup Instructions

Follow these steps to run the project locally:

1. **Clone the repository**  
   ```bash
   git clone <your-repo-url>
   cd <your-repo-directory>

2. **Create a .env file in the project root with the following variables:**  
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




## 📏 System Architecture

### 🚀 Overview

This system powers a sophisticated **hotel chatbot and admin management platform**. It's built on a robust architecture featuring a **FastAPI backend**, a dynamic **React frontend**, and seamless integration with the **Gemini LLM**.

### 🔹 Components

1.  **Frontend (React)**
    * **Chatbot UI (`Chatbot.jsx`):** The primary interface for guest interactions, handling all user input and displaying chatbot responses.
    * **Admin Dashboard (`AdminDashboard.jsx`):** A comprehensive panel for hotel staff to oversee and manage operations.
    * Handles all user input, displays responses, and communicates with backend APIs.

2.  **Backend (FastAPI)**
    * **API Endpoints:** Manages all core functionalities through dedicated endpoints like `/chat`, `/booking`, `/request`, and `/faq`.
    * **LLM Integration:** Utilizes **Gemini 1.5 Flash via LangChain** for processing natural language, generating responses, and performing sentiment analysis.
    * **Communication Services:** Integrates with **SendGrid** for email notifications and **Twilio** for SMS confirmations.
    * Performs sentiment analysis and generates AI summaries of chat interactions.

3.  **Database (Supabase)**
    * Serves as the central data repository for all chat logs, booking information, and room service requests.
    * Accessible and utilized by both the chatbot and the dashboard.

4.  **External Services**
    * **Gemini:** The core LLM responsible for intelligent chat responses and sentiment classification.
    * **Twilio:** Enables sending SMS notifications for room service requests and their resolution.
    * **SendGrid:** Facilitates sending email confirmations or rejections for booking requests.

### 🔄 Data Flow

1.  A guest initiates an interaction via the **chatbot UI**.
2.  The **frontend** sends the guest's request to the **FastAPI backend**.
3.  The **backend** processes the input, leveraging **Gemini** for AI capabilities and interacting with the **Supabase database** for data storage and retrieval.
4.  The processed response is then sent back to the **frontend UI** for display to the guest and is simultaneously stored in Supabase.
5.  The **admin dashboard** can retrieve and display all relevant data from Supabase for management purposes.




---

## 🔖 API Documentation

The following API endpoints facilitate communication between the frontend and backend, and manage data operations.

**Base URL:** `https://your-deployment-url`

---

### 📡 `/chat/`

* **`POST /chat/`**
    * **Description:** Sends a user message to the chatbot and saves the chat history along with sentiment.
    * **Request Body:**
        ```json
        {
          "user_id": "string",
          "message": "string"
        }
        ```
    * **Returns:**
        ```json
        {
          "response": "string"
        }
        ```

* **`GET /chat/sentiment-summary-ai`**
    * **Description:** Retrieves an AI-generated summary of chat sentiment.
    * **Returns:**
        ```json
        {
          "top_positive": "string",
          "top_negative": "string",
          "top_neutral": "string"
        }
        ```

---

### 📆 `/booking/`

* **`POST /booking/`**
    * **Description:** Submits a new room booking request.
    * **Request Body:**
        ```json
        {
          "user_id": "string",
          "name": "string",
          "room_type": "string",
          "check_in": "YYYY-MM-DD",
          "check_out": "YYYY-MM-DD"
        }
        ```
    * **Returns:**
        ```json
        {
          "message": "submitted!"
        }
        ```

* **`GET /booking/`**
    * **Description:** Fetches all existing room bookings.

* **`PATCH /booking/{id}/status`**
    * **Description:** Updates the status of a specific booking.
    * **Query Parameters:** `status` (can be `confirmed` or `rejected`)
    * **Example:** `/booking/123/status?status=confirmed`

* **`DELETE /booking/{id}`**
    * **Description:** Deletes a specific booking record.

* **`GET /booking/availability/`**
    * **Description:** Checks room availability for a given date range.
    * **Query Parameters:** `check_in=YYYY-MM-DD`, `check_out=YYYY-MM-DD`
    * **Returns:** Availability information by room type.

---

### 🛎 `/request/`

* **`POST /request/`**
    * **Description:** Submits a room service request, sends an SMS confirmation, and logs the request.
    * **Request Body:**
        ```json
        {
          "room_number": "string",
          "phone_number": "string",
          "request": "string"
        }
        ```

* **`GET /request/`**
    * **Description:** Fetches all outstanding room service requests.

* **`PATCH /request/{id}/resolve`**
    * **Description:** Marks a specific room service request as resolved.

* **`DELETE /request/{id}`**
    * **Description:** Deletes a specific room service request.

---

### 📖 `/faq/`

* **`GET /faq/`**
    * **Description:** Returns a list of hardcoded Frequently Asked Questions (currently 3 sample Q&A).

---   
