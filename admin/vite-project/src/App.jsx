import React, { useEffect } from "react";
import { useNavigate, Route, Routes } from "react-router-dom";
import Navbar from "./components/Navbar/Navbar";
import Sidebar from "./components/Sidebar/Sidebar";
import Login from "./pages/Login/Login";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import PromoCode from "./components/PromoCode/PromoCode";
import Add from "./pages/Add/Add"; // Import the Add component
import List from "./pages/List/List"; // Import the List component
import Orders from "./pages/Orders/Orders";

const App = () => {
  const navigate = useNavigate();
  const url = "http://localhost:8000";

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      navigate("/login");
    }
  }, [navigate]);

  return (
    <div>
      <ToastContainer />
      <Navbar />
      <hr />
      <div className="app-content">
        <Sidebar />
        <Routes>
          <Route path="/login" element={<Login url={url} />} />
          <Route path="/promocodes" element={<PromoCode url={url} />} />
          <Route path="/add" element={<Add url={url} />} />
          <Route path="/list" element={<List url={url} />} />{" "}
          <Route path="/orders" element={<Orders url={url} />} />
          {/* Add the List route */}
        </Routes>
      </div>
    </div>
  );
};

export default App;
