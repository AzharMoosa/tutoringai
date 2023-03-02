import { faGear, faRobot, faUser } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import MainContainer from '../../components/shared/MainContainer';
import { Page } from '../../data/pageConstants';
import './Settings.css';

const Settings = () => (
  <MainContainer current={Page.SETTINGS}>
    <div className="settings">
      <h2>Settings</h2>

      <div className="settings-link">
        <h3>General Settings</h3>
        <FontAwesomeIcon icon={faGear} />
      </div>

      <div className="settings-link">
        <h3>User Settings</h3>
        <FontAwesomeIcon icon={faUser} />
      </div>

      <div className="settings-link">
        <h3>Chatbot Settings</h3>
        <FontAwesomeIcon icon={faRobot} />
      </div>
    </div>
  </MainContainer>
);

export default Settings;
