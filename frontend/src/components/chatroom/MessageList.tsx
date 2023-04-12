import { useRef, useEffect } from 'react';
import MessageBubble from './MessageBubble';
import './MessageList.css';
import { Message } from './types';

type setMessageContentFunction = (messageContent: string) => void;

const MessageList = ({
  messageList,
  setMessageContent
}: {
  messageList: Array<Message>;
  setMessageContent: setMessageContentFunction;
}) => {
  const scrollRef = useRef<any>(null);

  const scrollToBottom = () => {
    scrollRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => scrollToBottom(), [messageList]);

  return (
    <div className="message-list">
      {messageList.map(({ messageContent, fromChatbot, question }, index) => (
        <MessageBubble
          key={Math.random()}
          messageContent={messageContent}
          fromChatbot={fromChatbot}
          question={question}
          setMessageContent={setMessageContent}
          isLatestMessage={index === messageList.length - 1}
        />
      ))}
      <div ref={scrollRef} />
    </div>
  );
};

export default MessageList;
