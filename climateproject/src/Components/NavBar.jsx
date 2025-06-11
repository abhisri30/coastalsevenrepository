import React from 'react';
import '../Styles/NavBar.css';
import CoastalSevenlogo from '../assets/CoastalSevenlogo.png';
import { Link } from 'react-router-dom';

const NavBar = () => {
  return (
    <div className="header">
      <img src={CoastalSevenlogo} alt="Logo" className="logo" />
      <div className="nav-links">
        <nav className="header-nav">
          <Link to="/about">About Us</Link>
          <Link to="/contact">Contact Us</Link>
          <Link to="/signin">Sign In</Link>
        </nav>
      </div>
    </div>
  );
};

export default NavBar;