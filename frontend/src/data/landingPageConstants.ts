export interface AboutInfo {
  title: string;
  icon: string;
  textContent: string;
}

export interface TopicInfo {
  title: string;
}

export interface ServiceDetails {
  title: string;
  description: string;
  boxOne: {
    title: string;
    description: string;
  };
  boxTwo: {
    title: string;
    description: string;
  };
  image: string;
  flipped: boolean;
}

export const topicBoxInfo: Array<TopicInfo> = [
  {
    title: 'ADDITION'
  },
  {
    title: 'TRIGONOMETRY'
  },
  {
    title: 'CIRCLES'
  },
  {
    title: 'RECTANGLES'
  },
  {
    title: 'MULTIPLICATION'
  },
  {
    title: 'DIVISION'
  }
];

export const aboutBoxInfo: Array<AboutInfo> = [
  {
    title: 'Intelligent Tutoring Chatbot',
    icon: 'robot',
    textContent:
      'Built using a large language model and leverages advanced AI capabilities to provide personalised educational support.'
  },
  {
    title: 'Mathematics',
    icon: 'calculator',
    textContent:
      'Equipped with mathematical knowledege which uses state-of-the-art deep-learning techniques to tutor a variety of different topics.'
  },
  {
    title: 'Feedback',
    icon: 'comment-dots',
    textContent:
      'Recieve feedback on areas of strengths and weaknesses to improve your understanding and knowledge about mathematics.'
  },
  {
    title: 'Personalised Tutoring',
    icon: 'person-chalkboard',
    textContent:
      'Trained using tutoring principles applied by human tutors, receive a personalised tutoring experience tailored to your needs.'
  },
  {
    title: 'Assessment Mode',
    icon: 'clipboard-list',
    textContent:
      'Test your current knowledge using the assessment mode to understand what areas of mathematics you require assistance on.'
  },
  {
    title: 'Revision Mode',
    icon: 'calendar-day',
    textContent:
      'Enhance your current knowledege using the revision mode by tackling new mathematical problems and working with the M.A.R.C to solve them.'
  }
];

export const serviceBoxInfo: Array<ServiceDetails> = [
  {
    title: 'Revision',
    description:
      'Revision mode is a feature designed to help users reinforce their understanding of key concepts. When activated, M.A.R.C presents targeted exercises and questions to the users, tailored to their individual learning needs. The user receives immediate feedback and guidance to address any mistakes or misconceptions.',
    boxOne: {
      title: 'Reinforcing Understanding',
      description:
        'By actively practicing and solving problems, users can deepen their comprehension and gain confidence in their mathematical abilities. The chatbot provides timely feedback, guiding users to correct any mistakes or misconceptions, and encourages them to engage in meaningful revision.'
    },
    boxTwo: {
      title: 'Active Learning and Mastery',
      description:
        'Through interactive exercises and challenges, users actively apply their knowledge, solve problems, and improve their problem-solving abilities. M.A.R.C offers immediate feedback, allowing users to identify areas of improvement and refine their approaches.'
    },
    image: '',
    flipped: false
  },
  {
    title: 'Assessment',
    description:
      "Assessment mode is used to evaluate user' knowledge and skills. It presents questions and exercises to assess their understanding of mathematical concepts and their ability to apply them. Users receive immediate feedback on their answers, highlighting correct solutions and explaining any mistakes. This helps users identify areas where they need improvement and enhances their mathematical reasoning. M.A.R.C also provides performance reports that summarize users' progress, showing their strengths and areas that need more attention.",
    boxOne: {
      title: 'Checking Knowledge and Progress',
      description:
        "Through various quizzes, M.A.R.C assesses users' understanding of mathematical concepts and measures their progress over time. Users are presented with questions that test their comprehension and application of mathematical principles."
    },
    boxTwo: {
      title: 'Feedback',
      description:
        'After users completes these assessments, M.A.R.C provides them with valuable feedback on their performance. This feedback includes explanations for correct solutions and guidance on any errors made. By understanding their mistakes, users can gain clarity, correct misconceptions, and deepen their understanding of mathematical concepts.'
    },
    image: '',
    flipped: true
  }
];
