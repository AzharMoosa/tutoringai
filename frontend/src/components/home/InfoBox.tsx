import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faRobot,
  faMessage,
  faRepeat
} from '@fortawesome/free-solid-svg-icons';
import './InfoBox.css';
import { AboutInfo } from '../../data/landingPageConstants';

const InfoBox = ({ info }: { info: AboutInfo }) => (
  <div className="info-box">
    <FontAwesomeIcon
      className="info-icon"
      icon={
        info.icon === 'robot'
          ? faRobot
          : info.icon === 'message'
          ? faMessage
          : info.icon === 'repeat'
          ? faRepeat
          : faRobot
      }
    />
    <h2>{info.title}</h2>
    <p>{info.textContent}</p>
  </div>
);

export default InfoBox;
