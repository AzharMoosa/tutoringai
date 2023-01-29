import React from 'react';
import './assets/App.css';
import Home from './pages/home/Home';
import Login from './pages/auth/Login';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import Register from './pages/auth/Register';

const router = createBrowserRouter([
  {
    path: '/',
    element: <Home />
  },
  {
    path: '/login',
    element: <Login />
  },
  {
    path: '/register',
    element: <Register />
  }
]);

const App = () => {
  return <RouterProvider router={router} />;
};

export default App;
