import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faRobot,
  faMessage,
  faRepeat,
  faCommentDots,
  faPersonChalkboard,
  faClipboardList,
  faCalendarDay,
  faCalculator
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
          : info.icon === 'comment-dots'
          ? faCommentDots
          : info.icon === 'person-chalkboard'
          ? faPersonChalkboard
          : info.icon === 'clipboard-list'
          ? faClipboardList
          : info.icon === 'calendar-day'
          ? faCalendarDay
          : info.icon === 'calculator'
          ? faCalculator
          : faRobot
      }
    />
    <h2>{info.title}</h2>
    <p>{info.textContent}</p>
  </div>
);

export default InfoBox;
