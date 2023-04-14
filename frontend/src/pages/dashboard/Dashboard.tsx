import MainContainer from '../../components/shared/MainContainer';
import { Page } from '../../data/pageConstants';
import { useAppDispatch, useAppSelector } from '../../hooks/redux/hooks';
import { getUser } from '../../features/user/userSlice';

import './Dashboard.css';
import { useEffect } from 'react';
import Loader, { LoaderType } from '../../components/shared/Loader';

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
        <h1>Dashboard</h1>
        {loading ? (
          <Loader loaderType={LoaderType.Oval} />
        ) : (
          <div>
            <h1>{userDetails?.fullName}</h1>
          </div>
        )}
      </div>
    </MainContainer>
  );
};

export default Dashboard;
