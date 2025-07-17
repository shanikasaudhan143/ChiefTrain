import React, { useState } from "react";
import axios from "axios";
import "./Chatbot.css";

function Chatbot() {
  const [section, setSection] = useState(null);

  // FAQ/chat
  const [faqInput, setFaqInput] = useState("");
  const [faqResponse, setFaqResponse] = useState("");

  // Request
  const [roomNumber, setRoomNumber] = useState("");
  const [phoneNumber, setPhoneNumber] = useState("");
  const [requestText, setRequestText] = useState("");
  const [requestSuccess, setRequestSuccess] = useState(false);

  // Booking
  const [email, setEmail] = useState("");
  const [roomType, setRoomType] = useState("Deluxe");
  const [checkIn, setCheckIn] = useState("");
  const [checkOut, setCheckOut] = useState("");
  const [bookingSuccess, setBookingSuccess] = useState("");

  const API_BASE = "https://chieftrain.onrender.com";

  // Voice Recognition
  const recognition =
    "webkitSpeechRecognition" in window
      ? new window.webkitSpeechRecognition()
      : null;

  const startListeningFaq = () => {
    if (!recognition) {
      alert("Speech Recognition not supported.");
      return;
    }
    recognition.lang = "en-US";
    recognition.start();

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      setFaqInput(transcript);
    };
  };

  const startListeningRequest = () => {
    if (!recognition) {
      alert("Speech Recognition not supported.");
      return;
    }
    recognition.lang = "en-US";
    recognition.start();

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      setRequestText(transcript);
    };
  };

  const speakResponse = (text) => {
    const synth = window.speechSynthesis;
    const utterance = new SpeechSynthesisUtterance(text);
    synth.speak(utterance);
  };

  // Submissions
  const handleFaqSubmit = async () => {
    if (!faqInput) return;
    const res = await axios.post(`${API_BASE}/chat/`, {
      user_id: email || "guest",
      message: faqInput,
    });
    setFaqResponse(res.data.response);
  };

  const handleRequestSubmit = async () => {
    if (!roomNumber || !phoneNumber || !requestText) {
      alert("Please fill all fields.");
      return;
    }
    await axios.post(`${API_BASE}/request/`, {
      room_number: roomNumber,
      phone_number: phoneNumber,
      request: requestText,
    });
    setRequestSuccess(true);
    setRequestText("");
  };

  const handleBookingSubmit = async () => {
    if (!email || !checkIn || !checkOut) {
      alert("Please fill all fields.");
      return;
    }
    await axios.post(`${API_BASE}/booking/`, {
      user_id: email,
      name: email,
      room_type: roomType,
      check_in: checkIn,
      check_out: checkOut,
    });
    setBookingSuccess("Booking request submitted! We will confirm via email.");
  };

  return (
    <div className="chatbot-container">
      <h2>🤖 How can I help you?</h2>

      {section === null && (
        <div className="chatbot-options">
          <button onClick={() => setSection("faq")}>Ask a Question</button>
          <button onClick={() => setSection("request")}>Request Room Service</button>
          <button onClick={() => setSection("booking")}>Booking Request</button>
        </div>
      )}

      {section === "faq" && (
        <div className="chatbot-section">
          <input
            value={faqInput}
            onChange={(e) => setFaqInput(e.target.value)}
            placeholder="Ask a question..."
          />
          <button onClick={handleFaqSubmit}>Ask</button>
          <button onClick={() => startListeningFaq()}>🎤 Record</button>
          <button onClick={() => setSection(null)}>⬅ Back</button>
          {faqResponse && (
            <div className="chatbot-response">
              <strong>Answer:</strong> {faqResponse}
              <button onClick={() => speakResponse(faqResponse)}>🔊 Read Aloud</button>
            </div>
          )}
        </div>
      )}

      {section === "request" && (
        <div className="chatbot-section">
          <input
            value={roomNumber}
            onChange={(e) => setRoomNumber(e.target.value)}
            placeholder="Room Number"
          />
          <input
            value={phoneNumber}
            onChange={(e) => setPhoneNumber(e.target.value)}
            placeholder="Phone Number"
          />
          <textarea
            value={requestText}
            onChange={(e) => setRequestText(e.target.value)}
            placeholder="Request (e.g., 2 towels)"
          />
          <button onClick={handleRequestSubmit}>Send Request</button>
          <button onClick={() => startListeningRequest()}>🎤 Record Request</button>
          <button onClick={() => setSection(null)}>⬅ Back</button>
          {requestSuccess && <p>Request sent successfully!</p>}
        </div>
      )}

      {section === "booking" && (
        <div className="chatbot-section">
          <input
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Your Email"
          />
          <select
            value={roomType}
            onChange={(e) => setRoomType(e.target.value)}
          >
            <option value="Deluxe">Deluxe</option>
            <option value="Suite">Suite</option>
            <option value="Standard">Standard</option>
          </select>
          <input
            type="date"
            value={checkIn}
            onChange={(e) => setCheckIn(e.target.value)}
          />
          <input
            type="date"
            value={checkOut}
            onChange={(e) => setCheckOut(e.target.value)}
          />
          <button onClick={handleBookingSubmit}>Request Booking</button>
          <button onClick={() => setSection(null)}>⬅ Back</button>
          {bookingSuccess && <p>{bookingSuccess}</p>}
        </div>
      )}
    </div>
  );
}

export default Chatbot;
