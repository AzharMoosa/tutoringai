import './DashboardTitle.css';

const DashboardTitle = ({ name }: { name: string }) => (
  <div className="dashboard-title-container">
    <h1>
      Welcome Back <span>{name}!</span>
    </h1>
  </div>
);

export default DashboardTitle;
