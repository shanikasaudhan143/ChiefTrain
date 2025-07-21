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
