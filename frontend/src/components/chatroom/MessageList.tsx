import React from 'react';
import MessageBubble from './MessageBubble';
import './MessageList.css';
import { Message } from './types';

const MessageList = ({ messageList }: { messageList: Array<Message> }) => {
  return (
    <div className="message-list">
      {messageList.map(({ messageContent, fromChatbot }) => (
        <MessageBubble
          key={Math.random()}
          messageContent={messageContent}
          fromChatbot={fromChatbot}
        />
      ))}
    </div>
  );
};

export default MessageList;
