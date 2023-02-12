import React from 'react';
import MainContainer from '../../components/shared/MainContainer';
import { Page } from '../../data/pageConstants';
import './Settings.css';

const Settings = () => {
  return (
    <MainContainer current={Page.SETTINGS}>
      <div className="settings">
        <h1>Settings</h1>
      </div>
    </MainContainer>
  );
};

export default Settings;
