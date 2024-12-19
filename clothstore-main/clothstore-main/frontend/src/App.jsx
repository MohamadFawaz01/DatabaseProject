import React, { useState } from "react";
import { Route, Routes } from "react-router-dom";
import Home from "./pages/Home/Home";
import Navbar from "./components/Navbar/Navbar";
import Footer from "./components/Footer/Footer";
import "./App.css";
import StoreContextProvider from "./context/StoreContext";
import LoginPopup from "./components/LoginPopup/LoginPopup";

const App = () => {
  const [showLogin, setShowLogin] = useState(false);

  return (
    <StoreContextProvider>
      {/* Popup is conditionally rendered */}
      {showLogin && <LoginPopup setShowLogin={setShowLogin} />}
      
      <div className="app">
        <Navbar setShowLogin={setShowLogin}/>
        <Routes>
          <Route path="/" element={<Home />} />
          {/* Add other routes if necessary */}
        </Routes>
      </div>
      <Footer />
    </StoreContextProvider>
  );
};

export default App;
