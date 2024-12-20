import React, { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import "./Login.css";

const Login = ({ url }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  // Clear the token when the login page loads
  useEffect(() => {
    localStorage.removeItem("token");
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("Submitting login request to:", `${url}/api/admin/login`);

    try {
      const response = await axios.post(`${url}/api/admin/login`, {
        username,
        password,
      });

      if (response.data.success) {
        localStorage.setItem("token", response.data.token); // Store the token
        navigate("/orders"); // Redirect to the orders page
      } else {
        alert(response.data.message); // Show error message
      }
    } catch (error) {
      console.error("Login error:", error);

      // Handle network errors
      if (error.response) {
        // Server responded with a status code out of 2xx range
        alert(
          `Error ${error.response.status}: ${
            error.response.data.detail || "Unknown error"
          }`
        );
      } else if (error.request) {
        // Request was made, but no response received
        alert("No response from server. Please check your connection.");
      } else {
        // Other errors
        alert("An unexpected error occurred. Please try again.");
      }
    }
  };

  return (
    <div className="login">
      <h2>Admin Login</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="username">Username</label>
          <input
            id="username"
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div>
          <label htmlFor="password">Password</label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default Login;
