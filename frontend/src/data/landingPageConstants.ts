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
      'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam auctor tortor vitae neque congue luctus. Donec sed elit nec lacus malesuada ornare. Sed non condimentum turpis. Vivamus imperdiet vel odio eget luctus. Vivamus viverra, urna et rhoncus luctus, libero dolor dapibus diam, et pulvinar justo metus sit amet tellus. Suspendisse eleifend, lacus ac molestie accumsan, neque nunc egestas tellus, luctus consectetur lorem quam sit amet nisi.',
    boxOne: {
      title: 'Heading One',
      description:
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam auctor tortor vitae neque congue luctus. Donec sed elit nec lacus malesuada ornare. Sed non condimentum turpis. Vivamus imperdiet vel odio eget luctus'
    },
    boxTwo: {
      title: 'Heading Two',
      description:
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam auctor tortor vitae neque congue luctus. Donec sed elit nec lacus malesuada ornare. Sed non condimentum turpis. Vivamus imperdiet vel odio eget luctus'
    },
    image: '',
    flipped: false
  },
  {
    title: 'Assessment',
    description:
      'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam auctor tortor vitae neque congue luctus. Donec sed elit nec lacus malesuada ornare. Sed non condimentum turpis. Vivamus imperdiet vel odio eget luctus. Vivamus viverra, urna et rhoncus luctus, libero dolor dapibus diam, et pulvinar justo metus sit amet tellus. Suspendisse eleifend, lacus ac molestie accumsan, neque nunc egestas tellus, luctus consectetur lorem quam sit amet nisi.',
    boxOne: {
      title: 'Heading One',
      description:
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam auctor tortor vitae neque congue luctus. Donec sed elit nec lacus malesuada ornare. Sed non condimentum turpis. Vivamus imperdiet vel odio eget luctus'
    },
    boxTwo: {
      title: 'Heading Two',
      description:
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam auctor tortor vitae neque congue luctus. Donec sed elit nec lacus malesuada ornare. Sed non condimentum turpis. Vivamus imperdiet vel odio eget luctus'
    },
    image: '',
    flipped: true
  }
];
