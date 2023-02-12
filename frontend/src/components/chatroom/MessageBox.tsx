import React, { useState, useEffect, useRef } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPaperPlane } from '@fortawesome/free-solid-svg-icons';
import './MessageBox.css';

type sendMessageFunction = (messageContent: string) => void;

const MessageBox = ({ sendMessage }: { sendMessage: sendMessageFunction }) => {
  const textAreaRef = useRef<any>(null);
  const messageInputRef = useRef<any>(null);
  const [messageContent, setMessageContent] = useState<string>('');

  useEffect(() => {
    // Resets To Original Height
    messageInputRef.current.style.height = '70px';

    // Adjust Height Using Text Content
    messageInputRef.current.style.height =
      textAreaRef.current.scrollHeight + 'px';
  }, [messageContent]);

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
      <div className="message-input" ref={messageInputRef}>
        <textarea
          ref={textAreaRef}
          className="message-textarea"
          value={messageContent}
          onChange={(e) => setMessageContent(e.target.value)}
          onKeyDown={(e) => handleEnterSubmit(e)}
        />
        <div className="send-btn">
          <FontAwesomeIcon
            onClick={handleSendMessage}
            className="send-btn-icon"
            icon={faPaperPlane}
          />
        </div>
      </div>
    </div>
  );
};

export default MessageBox;
