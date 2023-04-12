import { BLUE, PURPLE } from '../../data/colorConstants';
import {
  NumericalQuestion,
  MultipleChoiceQuestion,
  TrueOrFalseQuestion,
  QuestionType
} from '../../utils/chatRoomUtils';
import './MessageBubble.css';

type setMessageContentFunction = (messageContent: string) => void;

const messageBubbleStyle = (fromChatbot: boolean) => ({
  backgroundColor: fromChatbot ? PURPLE : BLUE
});

const DefaultMessageBubble = ({
  messageContent,
  fromChatbot
}: {
  messageContent: string;
  fromChatbot: boolean;
}) => (
  <>
    <div className="message-bubble" style={messageBubbleStyle(fromChatbot)}>
      <p>{messageContent}</p>
    </div>
  </>
);

const NumericalMessageBubble = ({
  messageContent,
  fromChatbot
}: {
  messageContent: string;
  fromChatbot: boolean;
}) => (
  <>
    <div className="message-bubble" style={messageBubbleStyle(fromChatbot)}>
      <p>{messageContent}</p>
    </div>
  </>
);

const TrueOrFalseMessageBubble = ({
  messageContent,
  fromChatbot,
  question
}: {
  messageContent: string;
  fromChatbot: boolean;
  question: TrueOrFalseQuestion;
}) => (
  <>
    <div className="message-bubble" style={messageBubbleStyle(fromChatbot)}>
      <p>{messageContent} true-or-false</p>
    </div>
  </>
);

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
  const selectOption = (option: string) => {
    setMessageContent(option);
  };

  return (
    <>
      <div className="message-bubble" style={messageBubbleStyle(fromChatbot)}>
        <p>{messageContent}</p>
        <div className="mcq-container">
          <div className="mcq-options">
            {question.options.map((option) => (
              <div
                onClick={() => isLatestMessage && selectOption(option)}
                key={Math.random()}
                className="mcq-option"
              >
                {option}
              </div>
            ))}
          </div>
        </div>
      </div>
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
