import React, { useState } from 'react';
import Button from '../../components/util/Button';
import Input from '../../components/util/Input';
import { GoogleLoginButton } from 'react-social-login-buttons';
import './AuthDetailsContainer.css';
import { Link } from 'react-router-dom';

const LoginDetailsContainer = () => {
  const [email, setEmail] = useState<string>('');
  const [password, setPassword] = useState<string>('');

  return (
    <div className="auth-container">
      <h2>Welcome Back</h2>
      <h4>Please enter your login details</h4>
      <Input
        name="email"
        type="email"
        placeholder="Email"
        value={email}
        setValue={setEmail}
      />
      <Input
        name="password"
        type="password"
        placeholder="Password"
        value={password}
        setValue={setPassword}
      />
      <br />
      <Button textContent="Login" small={true} />
      <div className="login-options">
        <div className="remember-me-container">
          <input type="checkbox" id="remember-me" />
          <label htmlFor="remember-me">Remember Me</label>
        </div>

        <h5 className="forgot-password">Forgot Password?</h5>
      </div>

      <div className="sign-in-social">
        <GoogleLoginButton onClick={() => alert('Hello')} />
      </div>
      <h4 className="no-account">
        Don't have an account?{' '}
        <span>
          <Link to="/register">Sign up for free</Link>
        </span>
      </h4>
    </div>
  );
};

export default LoginDetailsContainer;
