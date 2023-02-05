import React, { useState } from 'react';
import Button from '../../components/util/Button';
import Input from '../../components/util/Input';
import { GoogleLoginButton } from 'react-social-login-buttons';
import './AuthDetailsContainer.css';
import { Link } from 'react-router-dom';
import { useAppDispatch } from '../../hooks/redux/hooks';
import { loginUser } from '../../features/auth/authSlice';
import { Toaster } from 'react-hot-toast';
import { isLoginDetailsValid } from '../../services/auth/verifyAuthDetails';

const LoginDetailsContainer = () => {
  const [email, setEmail] = useState<string>('');
  const [password, setPassword] = useState<string>('');

  const dispatch = useAppDispatch();

  const login = () => {
    isLoginDetailsValid(email, password) &&
      dispatch(loginUser({ email, password }));
  };

  return (
    <div className="auth-container">
      <Toaster />
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
      <Button textContent="Login" small={true} onClick={() => login()} />
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
