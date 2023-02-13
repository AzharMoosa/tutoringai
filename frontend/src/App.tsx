import './assets/App.css';
import Home from './pages/home/Home';
import Login from './pages/auth/Login';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import Register from './pages/auth/Register';
import PrivateRoute from './components/util/routes/PrivateRoute';
import ChatRoom from './pages/chatroom/ChatRoom';
import AuthRoute from './components/util/routes/AuthRoute';
import Dashboard from './pages/dashboard/Dashboard';
import Settings from './pages/settings/Settings';

const router = createBrowserRouter([
  {
    path: '/',
    element: (
      <AuthRoute>
        <Home />
      </AuthRoute>
    )
  },
  {
    path: '/login',
    element: (
      <AuthRoute>
        <Login />
      </AuthRoute>
    )
  },
  {
    path: '/register',
    element: (
      <AuthRoute>
        <Register />
      </AuthRoute>
    )
  },
  {
    path: '/dashboard',
    element: (
      <PrivateRoute>
        <Dashboard />
      </PrivateRoute>
    )
  },
  {
    path: '/chatroom',
    element: (
      <PrivateRoute>
        <ChatRoom />
      </PrivateRoute>
    )
  },
  {
    path: '/settings',
    element: (
      <PrivateRoute>
        <Settings />
      </PrivateRoute>
    )
  }
]);

const App = () => {
  return <RouterProvider router={router} />;
};

export default App;
