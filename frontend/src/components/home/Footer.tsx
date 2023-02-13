import Title from '../util/Title';
import './Footer.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEnvelope } from '@fortawesome/free-solid-svg-icons';
const Footer = () => (
  <footer>
    <div className="container">
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
          <a href="#home">Home</a>
          <a href="#about">About</a>
          <a href="#topics">Topics</a>
          <a href="#services">Services</a>
          <a href="#contact">Contact</a>
          <a href="#login">Login</a>
          <a href="#register">Register</a>
        </div>
        <div className="get-in-touch">
          <h2>Get In Touch</h2>
          <div className="get-in-touch-email">
            <FontAwesomeIcon icon={faEnvelope} className="email-icon" />
            <h3>test@gmail.com</h3>
          </div>
        </div>
      </div>
    </div>
  </footer>
);

export default Footer;
