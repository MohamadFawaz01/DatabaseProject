import React from 'react';
import './Navbar.css';
import { assets } from '../../assets/assets';
import { useNavigate } from 'react-router-dom';

const Navbar = () => {
  const navigate = useNavigate();
  const token = localStorage.getItem('token'); // Get the token from localStorage

  const handleLogout = () => {
    localStorage.removeItem('token'); // Remove the token from localStorage
    navigate('/login'); // Redirect to the login page
  };

  return (
    <div>
      <div className='navbar'>
        <img className='logo' src={assets.new_logo} alt="Logo" />
        {token && ( // Only show the profile section if the token exists
          <div className='profile-section'>
            <img className='profile' src={assets.profile_image} alt="Profile" />
            <button className='logout-button' onClick={handleLogout}>
              Logout
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default Navbar;
