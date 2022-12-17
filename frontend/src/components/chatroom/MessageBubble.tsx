import React from 'react';
import { SECONDARY_LIGHT_BG, LIGHT_GRAY } from '../../data/colorConstants';
import './MessageBubble.css';

const messageBubbleStyle = (fromChatbot: boolean) => ({
  backgroundColor: fromChatbot ? SECONDARY_LIGHT_BG : LIGHT_GRAY,
  alignSelf: fromChatbot ? 'flex-start' : 'flex-end'
});

const MessageBubble = ({
  messageContent,
  fromChatbot
}: {
  messageContent: string;
  fromChatbot: boolean;
}) => {
  return (
    <div className="message-bubble" style={messageBubbleStyle(fromChatbot)}>
      <p>{messageContent}</p>
    </div>
  );
};

export default MessageBubble;
