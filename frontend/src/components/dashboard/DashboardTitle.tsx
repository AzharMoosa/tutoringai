import './DashboardTitle.css';

const DashboardTitle = ({ name }: { name: string }) => (
  <div className="dashboard-title-container">
    <h1>Welcome Back {name}!</h1>
  </div>
);

export default DashboardTitle;
