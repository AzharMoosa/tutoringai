import React from 'react';
import './Navbar.css';

const Navbar = () => {
  return (
    <div className="navbar-items">
      <a href="#home">Home</a>
      <a href="#about">About</a>
      <a href="#features">Features</a>
      <a href="#services">Services</a>
      <a href="#contact">Contact</a>
    </div>
  );
};

export default Navbar;
