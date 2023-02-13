import { BLUE, PURPLE } from '../../data/colorConstants';
import './MessageBubble.css';

const messageBubbleStyle = (fromChatbot: boolean) => ({
  backgroundColor: fromChatbot ? PURPLE : BLUE
});

const MessageBubble = ({
  messageContent,
  fromChatbot
}: {
  messageContent: string;
  fromChatbot: boolean;
}) => (
  <div className="message-bubble" style={messageBubbleStyle(fromChatbot)}>
    <p>{messageContent}</p>
  </div>
);

export default MessageBubble;
