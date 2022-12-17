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

  return (
    <div className="message-box">
      <textarea
        className="message-textarea"
        value={messageContent}
        onChange={(e) => setMessageContent(e.target.value)}
      ></textarea>
      <button onClick={handleSendMessage}>Send</button>
    </div>
  );
};

export default MessageBox;
