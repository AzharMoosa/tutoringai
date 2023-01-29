import React, { useState } from 'react';
import Button from '../../components/util/Button';
import Input from '../../components/util/Input';
import './AuthDetailsContainer.css';
import { Link } from 'react-router-dom';

const RegisterDetailsContainer = () => {
  const [fullName, setFullName] = useState<string>('');
  const [email, setEmail] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [confirmPassword, setConfirmPassword] = useState<string>('');

  return (
    <div className="auth-container">
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
      <Button textContent="Register" small={true} />
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
