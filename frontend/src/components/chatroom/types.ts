import { NumericalQuestion, MultipleChoiceQuestion, TrueOrFalseQuestion } from "../../utils/chatRoomUtils";

export type Message = {
  messageContent: string;
  fromChatbot: boolean;
  question: NumericalQuestion | MultipleChoiceQuestion | TrueOrFalseQuestion | undefined;
};
