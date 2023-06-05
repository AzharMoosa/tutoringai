import { RecentTopicDetails } from '../../features/user/userSlice';
import { AnsweringMode } from '../../features/user/userSlice';
import './RecentTopic.css';

const RecentTopic = ({ topic }: { topic: RecentTopicDetails }) => {
  return (
    <tr className="recent-topic">
      <td>{topic.mode === AnsweringMode.ASSESSMENT ? '-' : topic.topic}</td>
      <td>
        {topic.mode === AnsweringMode.ASSESSMENT ? 'Assessment' : 'Revision'}
      </td>
      {topic.mode === AnsweringMode.ASSESSMENT ? (
        <td>
          {topic.correctlyAnswered} / {topic.totalAnswered}
        </td>
      ) : (
        <td>{topic.totalAnswered}</td>
      )}
    </tr>
  );
};

export default RecentTopic;
