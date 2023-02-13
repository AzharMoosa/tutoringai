import { TopicInfo } from '../../data/landingPageConstants';
import './TopicBox.css';

const TopicBox = ({ info }: { info: TopicInfo }) => (
  <div className="topic-box">
    <h2>{info.title}</h2>
  </div>
);

export default TopicBox;
