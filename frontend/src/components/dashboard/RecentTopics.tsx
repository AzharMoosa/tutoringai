import { RecentTopicDetails } from '../../features/user/userSlice';
import RecentTopic from './RecentTopic';
import './RecentTopics.css';

const RecentTopics = ({
  topics,
  pageNumber
}: {
  topics: Array<RecentTopicDetails>;
  pageNumber: number;
}) => {
  const TOPICS_PER_PAGE = 10;
  const startingIndex = pageNumber * TOPICS_PER_PAGE;
  const endingIndex = pageNumber * TOPICS_PER_PAGE + TOPICS_PER_PAGE;

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
          {topics.slice(startingIndex, endingIndex).map((topic, index) => (
            <RecentTopic topic={topic} key={index} />
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default RecentTopics;
