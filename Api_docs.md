---

## 🔖 API Documentation

The following API endpoints facilitate communication between the frontend and backend, and manage data operations.

**Base URL:** `https://chieftrain.onrender.com`

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
