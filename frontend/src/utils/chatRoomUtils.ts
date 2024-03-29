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

export interface GraphicalQuestion {
  question: string;
  category: string;
}

export interface Triangle {
  a: number;
  b: number;
  c: number;
}

export interface Rectangle {
  width: number;
  height: number;
}

export interface Circle {
  radius: number;
}

export interface TriangleQuestion extends GraphicalQuestion {
  triangle: Triangle;
  questionType: string;
  topic: string;
  answer: number;
  imageUrl: string;
}

export interface RectangleQuestion extends GraphicalQuestion {
  rectangle: Rectangle;
  questionType: string;
  topic: string;
  answer: number;
  imageUrl: string;
}

export interface CircleQuestion extends GraphicalQuestion {
  circle: Circle;
  questionType: string;
  topic: string;
  answer: number;
  imageUrl: string;
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
    mode: string | undefined;
    correctAnswers: string | undefined;
    incorrectQuestions: number[];
    hintIndex: string | undefined;
    solution: string | undefined;
  };
}

export enum GraphicalType {
  Triangle = 'trigonometry',
  Rectangle = 'rectangles',
  Circle = 'circles',
  Undefined = 'undefined'
}

export enum QuestionType {
  Numerical = 'numerical',
  TrueOrFalse = 'true-or-false',
  MultipleChoice = 'mcq',
  Graphical = 'graphical',
  Undefined = 'undefined'
}

export const getGraphicsType = (category: string): GraphicalType => {
  switch (category) {
    case 'trigonometry':
      return GraphicalType.Triangle;
    case 'rectangles':
      return GraphicalType.Rectangle;
    case 'circles':
      return GraphicalType.Circle;
    default:
      return GraphicalType.Undefined;
  }
};

export const getQuestionType = (questionType: string): QuestionType => {
  switch (questionType) {
    case 'numerical':
      return QuestionType.Numerical;
    case 'true-or-false':
      return QuestionType.TrueOrFalse;
    case 'mcq':
      return QuestionType.MultipleChoice;
    case 'graphical':
      return QuestionType.Graphical;
    default:
      return QuestionType.Undefined;
  }
};
