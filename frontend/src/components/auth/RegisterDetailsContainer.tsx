import React, { useState } from 'react';
import Button from '../../components/util/Button';
import Input from '../../components/util/Input';
import './AuthDetailsContainer.css';
import { Link } from 'react-router-dom';
import { useAppDispatch } from '../../hooks/redux/hooks';
import { Toaster } from 'react-hot-toast';
import { registerUser } from '../../features/auth/authSlice';
import { isRegisterDetailsValid } from '../../services/auth/verifyAuthDetails';

const RegisterDetailsContainer = () => {
  const [fullName, setFullName] = useState<string>('');
  const [email, setEmail] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [confirmPassword, setConfirmPassword] = useState<string>('');

  const dispatch = useAppDispatch();

  const register = () => {
    isRegisterDetailsValid(fullName, email, password, confirmPassword) &&
      dispatch(registerUser({ email, fullName, password }));
  };

  return (
    <div className="auth-container">
      <Toaster />
      <h2>Get Started</h2>
      <h4>Please enter your details</h4>
      <Input
        name="fullName"
        type="text"
        placeholder="Full Name"
        value={fullName}
        setValue={setFullName}
      />
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
      <Input
        name="confirmPassword"
        type="password"
        placeholder="Confirm Password"
        value={confirmPassword}
        setValue={setConfirmPassword}
      />
      <div className="register-btn-layout">
        <Button textContent="Register" onClick={() => register()} />
      </div>

      <h4 className="no-account">
        Already have an account?
        <span>
          <Link to="/login">Login</Link>
        </span>
      </h4>
    </div>
  );
};

export default RegisterDetailsContainer;
