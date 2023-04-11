import React, { useEffect, useRef } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPaperPlane } from '@fortawesome/free-solid-svg-icons';
import './MessageBox.css';

type handleSendMessageFunction = () => void;
type setMessageContentFunction = (messageContent: string) => void;
type handleEnterSubmitFunction = (
  e: React.KeyboardEvent<HTMLTextAreaElement>
) => void;

const MessageBox = ({
  handleSendMessage,
  messageContent,
  setMessageContent,
  handleEnterSubmit
}: {
  handleSendMessage: handleSendMessageFunction;
  messageContent: string;
  setMessageContent: setMessageContentFunction;
  handleEnterSubmit: handleEnterSubmitFunction;
}) => {
  const textAreaRef = useRef<any>(null);
  const messageInputRef = useRef<any>(null);

  useEffect(() => {
    // Resets To Original Height
    messageInputRef.current.style.height = '70px';

    // Adjust Height Using Text Content
    messageInputRef.current.style.height =
      textAreaRef.current.scrollHeight + 'px';
  }, [messageContent]);

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
