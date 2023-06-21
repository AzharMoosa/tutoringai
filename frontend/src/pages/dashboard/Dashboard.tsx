import MainContainer from '../../components/shared/MainContainer';
import { Page } from '../../data/pageConstants';
import { useAppDispatch, useAppSelector } from '../../hooks/redux/hooks';
import { getUser } from '../../features/user/userSlice';

import './Dashboard.css';
import { useEffect, useState } from 'react';
import Loader, { LoaderType } from '../../components/shared/Loader';
import DashboardTitle from '../../components/dashboard/DashboardTitle';
import RecentTopics from '../../components/dashboard/RecentTopics';

const PreviousPageButton = ({
  pageNumber,
  previousPage
}: {
  pageNumber: number;
  previousPage: React.MouseEventHandler<HTMLHeadingElement>;
}) => (
  <h5
    style={{
      display: `${pageNumber === 0 ? 'none' : 'block'}`
    }}
    onClick={previousPage}
    className="previous-btn"
  >
    Prev
  </h5>
);

const NextPageButton = ({
  pageNumber,
  maximumPages,
  nextPage
}: {
  pageNumber: number;
  maximumPages: number;
  nextPage: React.MouseEventHandler<HTMLHeadingElement>;
}) => {
  const isLastPage = pageNumber === Math.ceil(maximumPages / 10) - 1;

  return (
    <h5
      style={{
        display: `${isLastPage ? 'none' : 'block'}`
      }}
      onClick={nextPage}
      className="next-btn"
    >
      Next
    </h5>
  );
};

const Dashboard = () => {
  const userDetails = useAppSelector((state) => state.user.userDetails);
  const loading = useAppSelector((state) => state.user.loading);

  const [pageNumber, setPageNumber] = useState<number>(0);

  const dispatch = useAppDispatch();

  useEffect(() => {
    dispatch(getUser());
  }, [dispatch, loading]);

  const nextPage = () => {
    setPageNumber((page) => page + 1);
  };

  const previousPage = () => {
    setPageNumber((page) => page - 1);
  };

  return (
    <MainContainer current={Page.DASHBOARD}>
      <div className="dashboard">
        {loading ? (
          <Loader loaderType={LoaderType.Oval} />
        ) : (
          <div className="dashboard-layout">
            <DashboardTitle name={userDetails?.fullName ?? ''} />
            <RecentTopics
              pageNumber={pageNumber}
              topics={userDetails?.recentTopics ?? []}
            />
            <div className="pagination">
              <PreviousPageButton
                pageNumber={pageNumber}
                previousPage={previousPage}
              />
              <NextPageButton
                maximumPages={userDetails?.recentTopics.length ?? 0}
                pageNumber={pageNumber}
                nextPage={nextPage}
              />
            </div>
          </div>
        )}
      </div>
    </MainContainer>
  );
};

export default Dashboard;
