import React, { useContext, useState, useEffect } from 'react';
import './Navbar.css';
import { assets } from '../../assets/assets';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { StoreContext } from '../../context/StoreContext';

const Navbar = ({ setShowLogin }) => {
  const [menu, setMenu] = useState("home");
  const { getTotalCartAmount, token, setToken } = useContext(StoreContext);
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    if (location.hash) {
      const element = document.getElementById(location.hash.substring(1));
      if (element) {
        // Adding a slight delay to ensure the element is in the DOM
        setTimeout(() => {
          element.scrollIntoView({ behavior: "smooth" });
        }, 100);
      }
    }
  }, [location]);

  const logout = () => {
    localStorage.removeItem("token");
    setToken("");
    navigate("/");
  };

  const isInmenuPage = location.pathname === '/Inmenu';

  return (
    <div className='Navbar'>
      <Link to='/'><img src={assets.new_logo} alt="" className="logo" /></Link>
      
      {/* Only display Navbar-menu if not on the /Inmenu page */}
      {!isInmenuPage && (
        <ul className="Navbar-menu">
          <Link to='/' onClick={() => setMenu("home")} className={menu === "home" ? "active" : ""}>home</Link>
          <Link
            to='/#explore-menu'
            onClick={() => setMenu("menu")}
            className={menu === "menu" ? "active" : ""}
          >
            menu
          </Link>
          <Link
            to='/#footer'
            onClick={() => setMenu("contact us")}
            className={menu === "contact us" ? "active" : ""}
          >
            contact us
          </Link>
        </ul>
      )}

      {!isInmenuPage && (
        <div className="Navbar-right">
          <div className="Navbar-search_icon">
            <Link to='cart'>
              <img src={assets.basket_icon} alt="" />
              <div className={getTotalCartAmount() === 0 ? "" : "dot"}></div>
            </Link>
          </div>
          <div>
            {!token ? (
              <button 
                onClick={() => setShowLogin(true)}
                className="login-button"
              >
                Sign in
              </button>
            ) : (
              <div className='navbar-profile'>
                <img src={assets.profile_icon} alt="" />
                <ul className="navbar-profile-dropdown">
                  <li onClick={() => navigate('/myorders')}><img src={assets.bag_icon} alt="" /><p>Orders</p></li>
                  <hr />
                  <li onClick={logout}><img src={assets.logout_icon} alt="" /><p>Logout</p></li>
                </ul>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default Navbar;
