import React from 'react';
import Sidebar from './Sidebar';
import './MainContainer.css';
import { Page } from '../../data/pageConstants';

const MainContainer = ({
  current,
  children
}: {
  current: Page;
  children: any;
}) => {
  return (
    <div className="main-container">
      <Sidebar current={current} />
      {children}
    </div>
  );
};

export default MainContainer;
