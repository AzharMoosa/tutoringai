import React from 'react';
import RegisterDetailsContainer from '../../components/auth/RegisterDetailsContainer';
import SplashScreen from '../../components/auth/SplashScreen';
import './Auth.css';

const Register = () => {
  return (
    <div className="auth-screen">
      <div className="auth-right">
        <RegisterDetailsContainer />
      </div>
      <SplashScreen />
    </div>
  );
};

export default Register;
