import { Topic } from '../../utils/dashboardUtils';
import './RecentTopic.css';

const RecentTopic = ({ topic }: { topic: Topic }) => {
  return (
    <tr className="recent-topic">
      <td>{topic.topic}</td>
      <td>
        {topic.totalSolved} / {topic.totalQuestions}
      </td>
    </tr>
  );
};

export default RecentTopic;
