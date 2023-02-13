import LoginDetailsContainer from '../../components/auth/LoginDetailsContainer';
import SplashScreen from '../../components/auth/SplashScreen';
import './Auth.css';

const Login = () => (
  <div className="auth-screen">
    <SplashScreen />
    <div className="auth-right">
      <LoginDetailsContainer />
    </div>
  </div>
);

export default Login;
