import { Navigate } from 'react-router-dom';
import { useAppSelector } from '../../../hooks/redux/hooks';

const PrivateRoute = ({ children }: { children: any }) => {
  const token = useAppSelector((state) => state.auth.token);
  return token ? children : <Navigate to="/login" />;
};

export default PrivateRoute;
