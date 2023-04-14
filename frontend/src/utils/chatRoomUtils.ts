import { Socket } from 'socket.io-client';
import { IUserDetails } from '../features/user/userSlice';

export interface Question {
  question: string;
  category: string;
  topic: string;
}

export interface NumericalQuestion extends Question {
  answer: number;
  questionType: string;
}

export interface MultipleChoiceQuestion extends Question {
  answer: number;
  options: string[];
  text: string;
  questionType: string;
}

export interface TrueOrFalseQuestion extends Question {
  answer: boolean;
  statement: string;
  questionType: string;
}

export interface ChatbotResponse {
  state: {
    message: string;
    isAnswering: boolean;
    currentQuestion:
      | NumericalQuestion
      | MultipleChoiceQuestion
      | TrueOrFalseQuestion
      | undefined;
    questionList:
      | (NumericalQuestion | MultipleChoiceQuestion | TrueOrFalseQuestion)[]
      | undefined;
    questionIndex: string | undefined;
  };
}

export enum QuestionType {
  Numerical = 'numerical',
  TrueOrFalse = 'true-or-false',
  MultipleChoice = 'mcq',
  Undefined = 'undefined'
}

export const startDefaultListeners = (socket: Socket) => {
  socket.io.on('reconnect', (attempt) => {
    console.info('Reconnected on attempt: ' + attempt);
  });

  socket.io.on('reconnect_attempt', (attempt) => {
    console.info('Reconnection attempt: ' + attempt);
  });

  socket.io.on('reconnect_error', (error) => {
    console.info('Reconnection Error: ' + error);
  });

  socket.io.on('reconnect_failed', () => {
    console.log('Reconnection failure');
    alert('Unable to connect to server');
  });
};

export const initialiseChatRoom = (
  socket: Socket,
  messageListener: (response: ChatbotResponse) => void,
  userDetails: IUserDetails | null
) => {
  socket.emit('join', {
    username: `${userDetails?.fullName ?? 'unknown'}`,
    room: `${userDetails?._id ?? 'unknown'}`
  });
  socket.on('received_message', messageListener);
};

export const getQuestionType = (questionType: string): QuestionType => {
  switch (questionType) {
    case 'numerical':
      return QuestionType.Numerical;
    case 'true-or-false':
      return QuestionType.TrueOrFalse;
    case 'mcq':
      return QuestionType.MultipleChoice;
    default:
      return QuestionType.Undefined;
  }
};
