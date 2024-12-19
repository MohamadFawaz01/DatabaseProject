// LoginPopup.jsx
import React, { useState, useContext } from 'react';
import './LoginPopup.css';
import { assets } from '../../assets/assets';
import { StoreContext } from '../../context/StoreContext';
import axios from "axios";

const LoginPopup = ({ setShowLogin }) => {
    const { url, setToken } = useContext(StoreContext);

    const [currState, setCurrState] = useState("Sign Up"); 
    const [data, setData] = useState({
        username: "",
        password: ""
    });
    const [showPassword, setShowPassword] = useState(false);
    const [feedbackMessage, setFeedbackMessage] = useState("");

    const onChangeHandler = (event) => {
        const { name, value } = event.target;
        setData(prevData => ({ ...prevData, [name]: value }));
    };

    const onLogin = async (event) => {
        event.preventDefault();
        const endpoint = currState === "Login" ? "/login/" : "/users/";

        const payload = {
            username: data.username,
            password: data.password
        };

        // For sign-up, add the fields required by your backend
        if (currState === "Sign Up") {
            payload.phone_number = "12345678";
            payload.address = "Some address";
        }

        try {
            const response = await axios.post(url + endpoint, payload);
            // If we get here, status is likely 2xx.
            // The backend returns a JSON with a "message" field.
            setFeedbackMessage(response.data.message);

            // Since the backend doesn't return a token, we can store a dummy token if needed.
            localStorage.setItem("token", "dummy-token");
            setToken("dummy-token");

            // Close popup on success
            setShowLogin(false);
        } catch (error) {
            // For errors, the backend likely returns 4xx with `detail` or some message.
            if (error.response) {
                setFeedbackMessage(error.response.data.detail || "An error occurred.");
            } else {
                setFeedbackMessage("An error occurred. Please try again.");
            }
        }
    };

    return (
        <div className='login-popup'>
            <form onSubmit={onLogin} className="login-popup-container">
                <div className="login-popup-title">
                    <h2>{currState}</h2>
                    <img onClick={() => setShowLogin(false)} src={assets.cross_icon} alt="Close" />
                </div>
                <div className="login-popup-inputs">
                    <input
                        name='username'
                        onChange={onChangeHandler}
                        value={data.username}
                        type="text"
                        placeholder='Your username'
                        required
                    />
                    <div className="password-field">
                        <input
                            name='password'
                            onChange={onChangeHandler}
                            value={data.password}
                            type={showPassword ? "text" : "password"}
                            placeholder='Password'
                            required
                        />
                        <button
                            type="button"
                            onClick={() => setShowPassword(prev => !prev)}
                            className="show-password-toggle"
                        >
                            {showPassword ? "Hide" : "Show"}
                        </button>
                    </div>
                </div>
                <button type='submit'>{currState === "Sign Up" ? "Create account" : "Log in"}</button>
                <div className="login-popup-condition">
                    <input type="checkbox" required />
                    <p>By continuing, I agree to the terms of use & privacy policy.</p>
                </div>
                {currState === "Login" ? (
                    <p>Create a new account? <span onClick={() => {setCurrState("Sign Up"); setFeedbackMessage('');}}>Click here</span></p>
                ) : (
                    <p>Already have an account? <span onClick={() => {setCurrState("Login"); setFeedbackMessage('');}}>Login here</span></p>
                )}

                {feedbackMessage && (
                    <p style={{marginTop: '20px', color: 'red'}}>{feedbackMessage}</p>
                )}
            </form>
        </div>
    );
};

export default LoginPopup;
