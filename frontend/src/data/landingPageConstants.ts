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
      'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam nec mi est. Cras lorem diam, feugiat ut aliquam eu, egestas et libero. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus aliquet elit eget est ultricies.'
  },
  {
    title: 'Intelligent Tutoring Chatbot',
    icon: 'robot',
    textContent:
      'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam nec mi est. Cras lorem diam, feugiat ut aliquam eu, egestas et libero. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus aliquet elit eget est ultricies.'
  },
  {
    title: 'Intelligent Tutoring Chatbot',
    icon: 'robot',
    textContent:
      'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam nec mi est. Cras lorem diam, feugiat ut aliquam eu, egestas et libero. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus aliquet elit eget est ultricies.'
  },
  {
    title: 'Intelligent Tutoring Chatbot',
    icon: 'robot',
    textContent:
      'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam nec mi est. Cras lorem diam, feugiat ut aliquam eu, egestas et libero. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus aliquet elit eget est ultricies.'
  },
  {
    title: 'Intelligent Tutoring Chatbot',
    icon: 'robot',
    textContent:
      'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam nec mi est. Cras lorem diam, feugiat ut aliquam eu, egestas et libero. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus aliquet elit eget est ultricies.'
  },
  {
    title: 'Intelligent Tutoring Chatbot',
    icon: 'robot',
    textContent:
      'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam nec mi est. Cras lorem diam, feugiat ut aliquam eu, egestas et libero. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus aliquet elit eget est ultricies.'
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
