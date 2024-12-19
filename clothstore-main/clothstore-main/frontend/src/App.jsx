// import React, { useState } from "react";
// import axios from "axios";

// const App = () => {
//   const [username, setUsername] = useState("");
//   const [password, setPassword] = useState("");
//   const [message, setMessage] = useState("");

//   const handleLogin = async (e) => {
//     e.preventDefault();
//     console.log("Attempting to log in with:", { username, password });

//     try {
//       const response = await axios.post("http://localhost:8001/login/", {
//         username: username,
//         password: password,
//       });
//       console.log("Response received:", response.data);
//       setMessage(response.data.message);
//     } catch (error) {
//       if (error.response) {
//         console.error("Error response from server:", error.response.data);
//         setMessage(error.response.data.detail);
//       } else if (error.request) {
//         console.error("No response received from server:", error.request);
//         setMessage("No response from server. Please try again.");
//       } else {
//         console.error("Unexpected error:", error.message);
//         setMessage("An unexpected error occurred. Please try again.");
//       }
//     }
//   };

//   return (
//     <div
//       style={{
//         maxWidth: "400px",
//         margin: "50px auto",
//         fontFamily: "Arial, sans-serif",
//       }}
//     >
//       <h1>Login</h1>
//       <form onSubmit={handleLogin}>
//         <div style={{ marginBottom: "20px" }}>
//           <label
//             htmlFor="username"
//             style={{ display: "block", marginBottom: "5px" }}
//           >
//             Username:
//           </label>
//           <input
//             type="text"
//             id="username"
//             value={username}
//             onChange={(e) => setUsername(e.target.value)}
//             required
//             style={{
//               width: "100%",
//               padding: "10px",
//               boxSizing: "border-box",
//               borderRadius: "5px",
//               border: "1px solid #ccc",
//             }}
//           />
//         </div>
//         <div style={{ marginBottom: "20px" }}>
//           <label
//             htmlFor="password"
//             style={{ display: "block", marginBottom: "5px" }}
//           >
//             Password:
//           </label>
//           <input
//             type="password"
//             id="password"
//             value={password}
//             onChange={(e) => setPassword(e.target.value)}
//             required
//             style={{
//               width: "100%",
//               padding: "10px",
//               boxSizing: "border-box",
//               borderRadius: "5px",
//               border: "1px solid #ccc",
//             }}
//           />
//         </div>
//         <button
//           type="submit"
//           style={{
//             width: "100%",
//             padding: "10px",
//             backgroundColor: "#007BFF",
//             color: "#fff",
//             border: "none",
//             borderRadius: "5px",
//             cursor: "pointer",
//           }}
//         >
//           Login
//         </button>
//       </form>

//       {message && (
//         <p
//           style={{
//             marginTop: "20px",
//             color: message.includes("Invalid") ? "red" : "green",
//           }}
//         >
//           {message}
//         </p>
//       )}
//     </div>
//   );
// };

// export default App;

import React, { useState } from "react";
import { Route, Routes } from "react-router-dom";
import Home from "./pages/Home/Home";
import Navbar from "./components/Navbar/Navbar";
import Footer from "./components/Footer/Footer";
import "./App.css";

// Import the StoreContextProvider and LoginPopup
import StoreContextProvider from "./context/StoreContext";
import LoginPopup from "./components/LoginPopup/LoginPopup";

const App = () => {
  const [showLogin, setShowLogin] = useState(false);

  return (
    <StoreContextProvider>
      <div className="app">
        <Navbar />
        {/* A temporary login button to open the login popup */}
        <div style={{ textAlign: "center", marginTop: "20px" }}>
          <button onClick={() => setShowLogin(true)}>
            Login / Register
          </button>
        </div>

        <Routes>
          <Route path="/" element={<Home />} />
        </Routes>
      </div>
      <Footer />

      {/* Conditionally render the LoginPopup */}
      {showLogin && <LoginPopup setShowLogin={setShowLogin} />}
    </StoreContextProvider>
  );
};

export default App;
