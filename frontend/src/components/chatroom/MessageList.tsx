import { useRef, useEffect } from 'react';
import MessageBubble from './MessageBubble';
import './MessageList.css';
import { Message } from './types';

const MessageList = ({ messageList }: { messageList: Array<Message> }) => {
  const scrollRef = useRef<any>(null);

  const scrollToBottom = () => {
    scrollRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => scrollToBottom(), [messageList]);

  return (
    <div className="message-list">
      {messageList.map(({ messageContent, fromChatbot, question }) => (
        <MessageBubble
          key={Math.random()}
          messageContent={messageContent}
          fromChatbot={fromChatbot}
          question={question}
        />
      ))}
      <div ref={scrollRef} />
    </div>
  );
};

export default MessageList;
