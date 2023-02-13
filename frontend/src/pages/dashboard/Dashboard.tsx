import MainContainer from '../../components/shared/MainContainer';
import { Page } from '../../data/pageConstants';
import './Dashboard.css';

const Dashboard = () => (
  <MainContainer current={Page.DASHBOARD}>
    <div className="dashboard">
      <h1>Dashboard</h1>
    </div>
  </MainContainer>
);

export default Dashboard;
