import MainContainer from '../../components/shared/MainContainer';
import { Page } from '../../data/pageConstants';
import { useAppDispatch, useAppSelector } from '../../hooks/redux/hooks';
import { getUser } from '../../features/user/userSlice';

import './Dashboard.css';
import { useEffect } from 'react';
import Loader, { LoaderType } from '../../components/shared/Loader';
import DashboardTitle from '../../components/dashboard/DashboardTitle';
import RecentTopics from '../../components/dashboard/RecentTopics';
import QuestionsSolved from '../../components/dashboard/QuestionsSolved';

const Dashboard = () => {
  const userDetails = useAppSelector((state) => state.user.userDetails);
  const loading = useAppSelector((state) => state.user.loading);

  const dispatch = useAppDispatch();

  useEffect(() => {
    dispatch(getUser());
  }, [dispatch, loading]);

  return (
    <MainContainer current={Page.DASHBOARD}>
      <div className="dashboard">
        {loading ? (
          <Loader loaderType={LoaderType.Oval} />
        ) : (
          <div className="dashboard-layout">
            <DashboardTitle name={userDetails?.fullName ?? ''} />
            <RecentTopics topics={userDetails?.recentTopics ?? []} />
            <div className="dashboard-grid">
              <QuestionsSolved />
              <QuestionsSolved />
              <QuestionsSolved />
            </div>
          </div>
        )}
      </div>
    </MainContainer>
  );
};

export default Dashboard;
