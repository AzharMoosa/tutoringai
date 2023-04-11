import { useRef, useEffect } from 'react';
import MessageBubble from './MessageBubble';
import './MessageList.css';
import { Message } from './types';

type handleSendMessageFunction = () => void;
type setMessageContentFunction = (messageContent: string) => void;

const MessageList = ({
  messageList,
  handleSendMessage,
  setMessageContent
}: {
  messageList: Array<Message>;
  handleSendMessage: handleSendMessageFunction;
  setMessageContent: setMessageContentFunction;
}) => {
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
          handleSendMessage={handleSendMessage}
          setMessageContent={setMessageContent}
        />
      ))}
      <div ref={scrollRef} />
    </div>
  );
};

export default MessageList;
