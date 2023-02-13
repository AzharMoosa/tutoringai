import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faBorderAll,
  faComment,
  faGear,
  faRightFromBracket
} from '@fortawesome/free-solid-svg-icons';
import './Sidebar.css';
import { Page } from '../../data/pageConstants';
import { Link } from 'react-router-dom';
import { useAppDispatch } from '../../hooks/redux/hooks';
import { logout } from '../../features/auth/authSlice';

const Sidebar = ({ current }: { current: Page }) => {
  const dispatch = useAppDispatch();

  return (
    <div className="sidebar">
      <div className="sidebar-items">
        <Link to={'/dashboard'}>
          <FontAwesomeIcon
            icon={faBorderAll}
            className={`${
              current === Page.DASHBOARD && 'highlight'
            } sidebar-item-icon`}
          />
        </Link>

        <Link to={'/chatroom'}>
          <FontAwesomeIcon
            icon={faComment}
            className={`${
              current === Page.CHATROOM && 'highlight'
            } sidebar-item-icon`}
          />
        </Link>
        <Link to={'/settings'}>
          <FontAwesomeIcon
            icon={faGear}
            className={`${
              current === Page.SETTINGS && 'highlight'
            } sidebar-item-icon`}
          />
        </Link>
      </div>

      <div className="sidebar-bottom-items">
        <FontAwesomeIcon
          icon={faRightFromBracket}
          className="sidebar-item-icon"
          onClick={() => dispatch(logout())}
        />
      </div>
    </div>
  );
};

export default Sidebar;
