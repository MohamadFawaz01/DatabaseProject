import React from "react";
import "./Footer.css";
import { assets } from "../../assets/assets";

const Footer = () => {
  return (
    <div className="footer" id="footer">
      <div className="footer-content">
        <div className="footer-content-left">
          <p>
            At Flava Diner, we believe in making every meal an experience. Join
            us on social media and stay connected for exclusive offers, new menu
            items, and more!
          </p>
          <div className="footer-social-icons">
            <a href="" target="_blank" rel="noopener noreferrer">
              <img src={assets.facebook_icon} alt="Facebook" />
            </a>
            <a href="" target="_blank" rel="noopener noreferrer">
              <img src={assets.tiktok_icon} alt="TikTok" />
            </a>
            <a href="" target="_blank" rel="noopener noreferrer">
              <img src={assets.instagram_icon} alt="Instagram" />
            </a>
          </div>
        </div>
        <div className="footer-content-center">
          <h2>OUR STORY</h2>
          <ul>
            <li>Home</li>
            <li>About Us</li>
            <li>Delivery Info</li>
            <li>Privacy Policy</li>
          </ul>
        </div>
        <div className="footer-content-right">
          <h2>CONTACT US</h2>
          <ul>
            <li>
              <a
                href=""
                target="_blank"
                rel="noopener noreferrer"
                className="whatsapp-link"
              >
                +961 03670970
              </a>
            </li>
          </ul>
        </div>
      </div>
      <hr />
      <p className="footer-copyright">
        © 2024 Flava Diner. All rights reserved.
      </p>
    </div>
  );
};

export default Footer;
