import React, { useState, useContext } from 'react';
import './LoginPopup.css'; // Uses the provided CSS
import { assets } from '../../assets/assets';
import { StoreContext } from '../../context/StoreContext';
import axios from "axios";

const LoginPopup = ({ setShowLogin }) => {
    const { url, setToken } = useContext(StoreContext);

    const [currState, setCurrState] = useState("Sign Up");
    const [data, setData] = useState({ username: "", password: "", phone_number: "", address: "" });
    const [showPassword, setShowPassword] = useState(false);
    const [feedbackMessage, setFeedbackMessage] = useState("");

    const onChangeHandler = (event) => {
        const { name, value } = event.target;
        setData(prevData => ({ ...prevData, [name]: value }));
    };

    const onLogin = async (event) => {
        event.preventDefault();
        const endpoint = currState === "Login" ? "/api/user/login" : "/api/user/register";

        const payload = {
            username: data.username,
            password: data.password
        };

        // Include phone_number and address only if signing up
        if (currState === "Sign Up") {
            payload.phone_number = data.phone_number;
            payload.address = data.address;
        }

        try {
            const response = await axios.post(url + endpoint, payload);
            if (response.data.success) {
                localStorage.setItem("token", response.data.token);
                setToken(response.data.token);
                setShowLogin(false);
            } else {
                setFeedbackMessage(response.data.message);
            }
        } catch (error) {
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
                    <img
                        onClick={() => setShowLogin(false)}
                        src={assets.cross_icon}
                        alt="Close"
                    />
                </div>
                <div className="login-popup-inputs">
                    {/* If Signing Up: show username, phone_number, address fields */}
                    {currState === "Sign Up" && (
                        <>
                            <input
                                name='username'
                                onChange={onChangeHandler}
                                value={data.username}
                                type="text"
                                placeholder='Your username'
                                required
                            />
                            <input
                                name='phone_number'
                                onChange={onChangeHandler}
                                value={data.phone_number}
                                type="text"
                                placeholder='Phone Number'
                                required
                            />
                            <input
                                name='address'
                                onChange={onChangeHandler}
                                value={data.address}
                                type="text"
                                placeholder='Address'
                                required
                            />
                        </>
                    )}

                    {/* If Logging In: show only username */}
                    {currState === "Login" && (
                        <input
                            name='username'
                            onChange={onChangeHandler}
                            value={data.username}
                            type="text"
                            placeholder='Your username'
                            required
                        />
                    )}

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
                    <p>Create a new account? <span onClick={() => { setCurrState("Sign Up"); setFeedbackMessage(''); }}>Click here</span></p>
                ) : (
                    <p>Already have an account? <span onClick={() => { setCurrState("Login"); setFeedbackMessage(''); }}>Login here</span></p>
                )}

                {feedbackMessage && (
                    <p style={{ marginTop: '20px', color: 'red' }}>{feedbackMessage}</p>
                )}
            </form>
        </div>
    );
};

export default LoginPopup;
