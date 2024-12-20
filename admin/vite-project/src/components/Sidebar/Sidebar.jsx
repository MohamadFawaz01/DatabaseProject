import React from 'react';
import './Sidebar.css';
import { assets } from '../../assets/assets';
import { NavLink } from 'react-router-dom';

const Sidebar = () => {
  return (
    <div className='sidebar'>
      <div className="sidebar-options">
        <NavLink to='/add' className="sidebar-option">
          <img src={assets.add_icon} alt="Add Items" />
          <p>Add Items</p>
        </NavLink>
        <NavLink to='/list' className="sidebar-option">
          <img src={assets.order_icon} alt="List Items" />
          <p>List Items</p>
        </NavLink>
        <NavLink to='/orders' className="sidebar-option">
          <img src={assets.order_icon} alt="Orders" />
          <p>Orders</p>
        </NavLink>
        <NavLink to='/delivered-items' className="sidebar-option">
          <img src={assets.order_icon} alt="Delivered Items" />
          <p>Delivered Items</p>
        </NavLink>
        <NavLink to='/promocodes' className="sidebar-option"> {/* New promo codes link */}
          <img src={assets.add_icon} alt="Promo Codes" />
          <p>Promo Codes</p>
        </NavLink>
      </div>
    </div>
  );
};

export default Sidebar;
