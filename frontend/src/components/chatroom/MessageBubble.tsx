import { BLUE, PURPLE } from '../../data/colorConstants';
import {
  NumericalQuestion,
  MultipleChoiceQuestion,
  TrueOrFalseQuestion,
  QuestionType
} from '../../utils/chatRoomUtils';
import './MessageBubble.css';

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
  question
}: {
  messageContent: string;
  fromChatbot: boolean;
  question: MultipleChoiceQuestion;
}) => (
  <>
    <div className="message-bubble" style={messageBubbleStyle(fromChatbot)}>
      <p>
        {messageContent} {question.options}
      </p>
    </div>
  </>
);

const messageBubbleLayout = (
  messageContent: string,
  fromChatbot: boolean,
  question:
    | NumericalQuestion
    | MultipleChoiceQuestion
    | TrueOrFalseQuestion
    | undefined
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
  question
}: {
  messageContent: string;
  fromChatbot: boolean;
  question:
    | NumericalQuestion
    | MultipleChoiceQuestion
    | TrueOrFalseQuestion
    | undefined;
}) => messageBubbleLayout(messageContent, fromChatbot, question);

export default MessageBubble;
