import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faRobot,
  faMessage,
  faRepeat
} from '@fortawesome/free-solid-svg-icons';
import './InfoBox.css';

interface InfoBoxStyle {
  title: string;
  icon: string;
  textContent: string;
}

const InfoBox = ({ title, icon, textContent }: InfoBoxStyle) => {
  return (
    <div className="info-box">
      <h2>{title}</h2>
      <FontAwesomeIcon
        className="info-icon"
        icon={
          icon === 'robot'
            ? faRobot
            : icon === 'message'
            ? faMessage
            : icon === 'repeat'
            ? faRepeat
            : faRobot
        }
      />
      <p>{textContent}</p>
    </div>
  );
};

export default InfoBox;
