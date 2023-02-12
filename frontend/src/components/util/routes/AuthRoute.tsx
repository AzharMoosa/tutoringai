import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAppSelector } from '../../../hooks/redux/hooks';

const AuthRoute = ({ children }: { children: any }) => {
  const token = useAppSelector((state) => state.auth.token);
  return token ? <Navigate to="/dashboard" /> : children;
};

export default AuthRoute;
