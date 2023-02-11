import React, { useState } from 'react';
import './MessageBox.css';

type sendMessageFunction = (messageContent: string) => void;

const MessageBox = ({ sendMessage }: { sendMessage: sendMessageFunction }) => {
  const [messageContent, setMessageContent] = useState<string>('');

  const handleSendMessage = () => {
    if (messageContent !== '') {
      sendMessage(messageContent);
      setMessageContent('');
    }
  };

  const handleEnterSubmit = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && e.shiftKey === false) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="message-box">
      <textarea
        className="message-textarea"
        value={messageContent}
        onChange={(e) => setMessageContent(e.target.value)}
        onKeyDown={(e) => handleEnterSubmit(e)}
      />
      <button onClick={handleSendMessage}>Send</button>
    </div>
  );
};

export default MessageBox;
