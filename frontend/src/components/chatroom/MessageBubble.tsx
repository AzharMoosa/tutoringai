import { BLUE, PURPLE } from '../../data/colorConstants';
import {
  NumericalQuestion,
  MultipleChoiceQuestion,
  TrueOrFalseQuestion,
  QuestionType,
  TriangleQuestion,
  RectangleQuestion,
  CircleQuestion
} from '../../utils/chatRoomUtils';
import MessageTextBlock from '../util/MessageTextBlock';
import './MessageBubble.css';
import { useState, useEffect } from 'react';

type setMessageContentFunction = (messageContent: string) => void;

const typingSpeed = 15;

const NEWBOX_PATTERN = /<newbox\s*\/?\s*>/g;

const messageBubbleStyle = (fromChatbot: boolean) => ({
  backgroundColor: fromChatbot ? PURPLE : BLUE
});

const DefaultMessageBubble = ({
  messageContent,
  fromChatbot
}: {
  messageContent: string;
  fromChatbot: boolean;
}) => {
  const [messageText, setMessageText] = useState('');

  useEffect(() => {
    const typingEffect = setInterval(() => {
      setMessageText(messageContent.slice(0, messageText.length + 1));
    }, typingSpeed);

    return () => clearInterval(typingEffect);
  }, [messageContent, messageText]);

  const boxes = messageText
    .split(NEWBOX_PATTERN)
    .map((message) => message.trim())
    .filter((message) => message !== '');

  return (
    <>
      {boxes.map((message, index) => (
        <div
          key={index}
          className="message-bubble"
          style={messageBubbleStyle(fromChatbot)}
        >
          <MessageTextBlock text={fromChatbot ? message : messageContent} />
        </div>
      ))}
    </>
  );
};

const NumericalMessageBubble = ({
  messageContent,
  fromChatbot
}: {
  messageContent: string;
  fromChatbot: boolean;
}) => {
  const [messageText, setMessageText] = useState('');

  useEffect(() => {
    const typingEffect = setInterval(() => {
      setMessageText(messageContent.slice(0, messageText.length + 1));
    }, typingSpeed);

    return () => clearInterval(typingEffect);
  }, [messageContent, messageText]);

  const boxes = messageText
    .split(NEWBOX_PATTERN)
    .map((message) => message.trim())
    .filter((message) => message !== '');

  return (
    <>
      {boxes.map((message, index) => (
        <div
          key={index}
          className="message-bubble"
          style={messageBubbleStyle(fromChatbot)}
        >
          <MessageTextBlock text={message} />
        </div>
      ))}
    </>
  );
};

const TrueOrFalseMessageBubble = ({
  messageContent,
  fromChatbot,
  question,
  setMessageContent,
  isLatestMessage
}: {
  messageContent: string;
  fromChatbot: boolean;
  question: TrueOrFalseQuestion;
  setMessageContent: setMessageContentFunction;
  isLatestMessage: boolean;
}) => {
  const [messageText, setMessageText] = useState('');

  useEffect(() => {
    const typingEffect = setInterval(() => {
      setMessageText(messageContent.slice(0, messageText.length + 1));
    }, typingSpeed);

    return () => clearInterval(typingEffect);
  }, [messageContent, messageText]);

  const selectOption = (option: string) => {
    setMessageContent(option);
  };

  const boxes = messageText
    .split(NEWBOX_PATTERN)
    .map((message) => message.trim())
    .filter((message) => message !== '');

  return (
    <>
      {boxes.map((message, index) => (
        <div
          key={index}
          className="message-bubble"
          style={messageBubbleStyle(fromChatbot)}
        >
          <MessageTextBlock text={message} />
          {message.length === messageContent.length && (
            <div className="true-or-false-container">
              <p>{question.statement}</p>
              <div className="true-or-false-options">
                {['True', 'False'].map((option, index) => (
                  <div
                    onClick={() => isLatestMessage && selectOption(option)}
                    key={index}
                    className="mcq-option"
                  >
                    {option}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      ))}
    </>
  );
};

const MultipleChoiceMessageBubble = ({
  messageContent,
  fromChatbot,
  question,
  setMessageContent,
  isLatestMessage
}: {
  messageContent: string;
  fromChatbot: boolean;
  question: MultipleChoiceQuestion;
  setMessageContent: setMessageContentFunction;
  isLatestMessage: boolean;
}) => {
  const [messageText, setMessageText] = useState('');

  useEffect(() => {
    const typingEffect = setInterval(() => {
      setMessageText(messageContent.slice(0, messageText.length + 1));
    }, typingSpeed);

    return () => clearInterval(typingEffect);
  }, [messageContent, messageText]);

  const selectOption = (option: string) => {
    setMessageContent(option);
  };

  const boxes = messageText
    .split(NEWBOX_PATTERN)
    .map((message) => message.trim())
    .filter((message) => message !== '');

  return (
    <>
      {boxes.map((message, index) => (
        <div
          key={index}
          className="message-bubble"
          style={messageBubbleStyle(fromChatbot)}
        >
          <MessageTextBlock text={message} />
          {message.length === messageContent.length && (
            <div className="mcq-container">
              <div className="mcq-options">
                {question.options.map((option, index) => (
                  <div
                    onClick={() => isLatestMessage && selectOption(option)}
                    key={index}
                    className="mcq-option"
                  >
                    {option}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      ))}
    </>
  );
};

const GraphicalQuestionMessageBubble = ({
  messageContent,
  fromChatbot,
  question
}: {
  messageContent: string;
  fromChatbot: boolean;
  question: TriangleQuestion | RectangleQuestion | CircleQuestion;
}) => {
  const [messageText, setMessageText] = useState('');

  useEffect(() => {
    const typingEffect = setInterval(() => {
      setMessageText(messageContent.slice(0, messageText.length + 1));
    }, typingSpeed);

    return () => clearInterval(typingEffect);
  }, [messageContent, messageText]);

  const boxes = messageText
    .split(NEWBOX_PATTERN)
    .map((message) => message.trim())
    .filter((message) => message !== '');

  return (
    <>
      {boxes.map((message, index) => (
        <div
          key={index}
          className="message-bubble"
          style={messageBubbleStyle(fromChatbot)}
        >
          <MessageTextBlock text={message} />
          <div className="graphics-image-container">
            {message.length === messageContent.length && (
              <img src={question.imageUrl} alt="shape" />
            )}
          </div>
        </div>
      ))}
    </>
  );
};

const messageBubbleLayout = (
  messageContent: string,
  fromChatbot: boolean,
  question:
    | NumericalQuestion
    | MultipleChoiceQuestion
    | TrueOrFalseQuestion
    | TriangleQuestion
    | undefined,
  setMessageContent: setMessageContentFunction,
  isLatestMessage: boolean
) => {
  switch (question?.questionType) {
    case QuestionType.Numerical:
      return (
        <NumericalMessageBubble
          messageContent={messageContent}
          fromChatbot={fromChatbot}
        />
      );
    case QuestionType.TrueOrFalse:
      return (
        <TrueOrFalseMessageBubble
          messageContent={messageContent}
          fromChatbot={fromChatbot}
          question={question as TrueOrFalseQuestion}
          setMessageContent={setMessageContent}
          isLatestMessage={isLatestMessage}
        />
      );
    case QuestionType.MultipleChoice:
      return (
        <MultipleChoiceMessageBubble
          messageContent={messageContent}
          fromChatbot={fromChatbot}
          question={question as MultipleChoiceQuestion}
          setMessageContent={setMessageContent}
          isLatestMessage={isLatestMessage}
        />
      );
    case QuestionType.Graphical:
      return (
        <GraphicalQuestionMessageBubble
          messageContent={messageContent}
          fromChatbot={fromChatbot}
          question={question as TriangleQuestion}
        />
      );
    default:
      return (
        <DefaultMessageBubble
          messageContent={messageContent}
          fromChatbot={fromChatbot}
        />
      );
  }
};

const MessageBubble = ({
  messageContent,
  fromChatbot,
  question,
  setMessageContent,
  isLatestMessage
}: {
  messageContent: string;
  fromChatbot: boolean;
  question:
    | NumericalQuestion
    | MultipleChoiceQuestion
    | TrueOrFalseQuestion
    | TriangleQuestion
    | undefined;
  setMessageContent: setMessageContentFunction;
  isLatestMessage: boolean;
}) =>
  messageBubbleLayout(
    messageContent,
    fromChatbot,
    question,
    setMessageContent,
    isLatestMessage
  );

export default MessageBubble;
