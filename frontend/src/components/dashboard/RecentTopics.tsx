import { Topic } from '../../utils/dashboardUtils';
import RecentTopic from './RecentTopic';
import './RecentTopics.css';

const RecentTopics = ({ topics }: { topics: Array<Topic> }) => {
  const topN = 10;

  return (
    <div className="recent-topics">
      <h2>Recent Topics</h2>
      <table className="recent-topics-table">
        <thead>
          <tr>
            <th>Topic</th>
            <th>Solved Questions</th>
          </tr>
        </thead>
        <tbody>
          {topics.slice(0, topN).map((topic) => (
            <RecentTopic topic={topic} key={Math.random()} />
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default RecentTopics;
