import React from 'react';
import Title from '../util/Title';

const Footer = () => {
  return (
    <footer>
      <div className="footer-left">
        <Title />
        <p>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce vel
          vestibulum ante. Vivamus aliquet a libero ut cursus. Mauris
          ullamcorper posuere ex non ultricies. Aliquam congue mi finibus
          pharetra finibus.
        </p>
      </div>
      <div className="footer-right">
        <div className="quick-links">
          <h2>Quick Links</h2>
          <h3>Home</h3>
          <h3>About</h3>
          <h3>Features</h3>
          <h3>Services</h3>
          <h3>Contact</h3>
          <h3>Login</h3>
          <h3>Register</h3>
        </div>
        <div className="get-in-touch">
          <h2>Get In Touch</h2>
          <div className="get-in-touch-email">
            <h3>test@gmail.com</h3>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
