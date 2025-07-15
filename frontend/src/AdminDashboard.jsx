import React, { useEffect, useState } from "react";
import axios from "axios";
import "./AdminDashboard.css";

function AdminDashboard() {
  const [password, setPassword] = useState("");
  const [authenticated, setAuthenticated] = useState(false);

  const [requests, setRequests] = useState([]);
  const [bookings, setBookings] = useState([]);

  const API_BASE = "http://localhost:8000";

  const fetchData = async () => {
    const reqRes = await axios.get(`${API_BASE}/request/`);
    const bookRes = await axios.get(`${API_BASE}/booking/`);
    setRequests(reqRes.data.requests);
    setBookings(bookRes.data.bookings);
  };

  useEffect(() => {
    if (authenticated) {
      fetchData();
    }
  }, [authenticated]);

  const handleLogin = () => {
    // This is where you define your admin password
    if (password === "hotel@123") {
      setAuthenticated(true);
    } else {
      alert("Incorrect password");
    }
  };

  const resolveRequest = async (id) => {
    await axios.patch(`${API_BASE}/request/${id}/resolve`);
    fetchData();
  };

  const updateBooking = async (id, status) => {
    await axios.patch(`${API_BASE}/booking/${id}/status?status=${status}`);
    fetchData();
  };

  if (!authenticated) {
    return (
      <div className="dashboard-container">
        <h2>Admin Login</h2>
        <input
          type="password"
          placeholder="Enter admin password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button onClick={handleLogin}>Login</button>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      <h2>Admin Dashboard</h2>

      <h3>Room Service Requests</h3>
      {requests.length === 0 ? (
        <p>No requests.</p>
      ) : (
        <table className="dashboard-table">
          <thead>
            <tr>
              <th>Room</th>
              <th>Phone</th>
              <th>Request</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {requests.map((r) => (
              <tr key={r.id}>
                <td data-label="Room">{r.room_number}</td>
                <td data-label="Phone">{r.phone_number}</td>
                <td data-label="Request">{r.request}</td>
                <td data-label="Status">{r.status}</td>
                <td data-label="Action">
                  {r.status === "pending" && (
                    <button onClick={() => resolveRequest(r.id)}>Resolve</button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>

        </table>
      )}

      <h3>Booking Requests</h3>
      {bookings.length === 0 ? (
        <p>No bookings.</p>
      ) : (
        <table className="dashboard-table">
          <thead>
            <tr>
              <th>Email</th>
              <th>Name</th>
              <th>Room</th>
              <th>Dates</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
          {bookings.map((b) => (
            <tr key={b.id}>
              <td data-label="Email">{b.user_id}</td>
              <td data-label="Name">{b.name}</td>
              <td data-label="Room">{b.room_type}</td>
              <td data-label="Dates">{b.check_in} to {b.check_out}</td>
              <td data-label="Status">{b.status}</td>
              <td data-label="Actions">
                {b.status === "pending" && (
                  <>
                    <button onClick={() => updateBooking(b.id, "confirmed")}>Confirm</button>
                    <button onClick={() => updateBooking(b.id, "rejected")}>Reject</button>
                  </>
                )}
              </td>
            </tr>
          ))}
        </tbody>

        </table>
      )}
    </div>
  );
}

export default AdminDashboard;
