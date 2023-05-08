import GeneralSettingsOptions from '../../components/settings/GeneralSettingsOptions';
import MainContainer from '../../components/shared/MainContainer';
import { Page } from '../../data/pageConstants';
import './Settings.css';
import { useAppDispatch, useAppSelector } from '../../hooks/redux/hooks';
import { useEffect } from 'react';
import { getUser } from '../../features/user/userSlice';

const Settings = () => {
  const userDetails = useAppSelector((state) => state.user.userDetails);
  const loading = useAppSelector((state) => state.user.loading);
  const dispatch = useAppDispatch();

  useEffect(() => {
    dispatch(getUser());
  }, [dispatch, loading]);

  return (
    <MainContainer current={Page.SETTINGS}>
      {!loading && userDetails && (
        <div className="settings">
          <div className="settings-link">
            <GeneralSettingsOptions userDetails={userDetails} />
          </div>
        </div>
      )}
    </MainContainer>
  );
};

export default Settings;
