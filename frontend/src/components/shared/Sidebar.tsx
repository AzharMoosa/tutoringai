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
import Title from '../util/Title';

const Sidebar = ({ current }: { current: Page }) => {
  const dispatch = useAppDispatch();

  return (
    <div className="sidebar">
      <div className="sidebar-top">
        <div className="sidebar-title">
          <Title />
        </div>
        <div className="sidebar-items">
          <Link to={'/dashboard'}>
            <div className="sidebar-item">
              <FontAwesomeIcon
                icon={faBorderAll}
                className={`${
                  current === Page.DASHBOARD && 'highlight'
                } sidebar-item-icon`}
              />
              <h2 className={current === Page.DASHBOARD ? 'highlight' : ''}>
                Dashboard
              </h2>
            </div>
          </Link>

          <Link to={'/chatroom'}>
            <div className="sidebar-item">
              <FontAwesomeIcon
                icon={faComment}
                className={`${
                  current === Page.CHATROOM && 'highlight'
                } sidebar-item-icon`}
              />
              <h2 className={current === Page.CHATROOM ? 'highlight' : ''}>
                M.A.R.C
              </h2>
            </div>
          </Link>
          <Link to={'/settings'}>
            <div className="sidebar-item">
              <FontAwesomeIcon
                icon={faGear}
                className={`${
                  current === Page.SETTINGS && 'highlight'
                } sidebar-item-icon`}
              />
              <h2 className={current === Page.SETTINGS ? 'highlight' : ''}>
                Settings
              </h2>
            </div>
          </Link>
        </div>
      </div>

      <div className="sidebar-bottom-items">
        <div className="sidebar-item" onClick={() => dispatch(logout())}>
          <FontAwesomeIcon
            icon={faRightFromBracket}
            className="sidebar-item-icon"
          />
          <h2>Log Out</h2>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
