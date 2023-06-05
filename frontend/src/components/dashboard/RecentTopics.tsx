import { RecentTopicDetails } from '../../features/user/userSlice';
import RecentTopic from './RecentTopic';
import './RecentTopics.css';

const RecentTopics = ({ topics }: { topics: Array<RecentTopicDetails> }) => {
  const topN = 5;

  return (
    <div className="recent-topics">
      <h2>Recent Topics</h2>
      <table className="recent-topics-table">
        <thead>
          <tr>
            <th>Topic</th>
            <th>Type</th>
            <th>Solved Questions</th>
          </tr>
        </thead>
        <tbody>
          {topics.slice(0, topN).map((topic, index) => (
            <RecentTopic topic={topic} key={index} />
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default RecentTopics;
