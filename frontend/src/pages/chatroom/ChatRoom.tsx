import { useState, useEffect } from 'react';
import './ChatRoom.css';
import MessageBox from '../../components/chatroom/MessageBox';
import MessageList from '../../components/chatroom/MessageList';
import { Message } from '../../components/chatroom/types';
import { useSocket } from '../../hooks/socket/hooks';
import {
  DEFAULT_MESSAGE,
  WEB_SOCKET_URI,
  WEB_SOCKET_CONFIG
} from '../../data/chatRoomConstants';
import {
  ChatbotResponse,
  startDefaultListeners,
  initialiseChatRoom,
  Question,
  TrueOrFalseQuestion,
  MultipleChoiceQuestion,
  NumericalQuestion
} from '../../utils/chatRoomUtils';
import MainContainer from '../../components/shared/MainContainer';
import { Page } from '../../data/pageConstants';

const ChatRoom = () => {
  const socket = useSocket(WEB_SOCKET_URI, WEB_SOCKET_CONFIG);
  const [isAnswering, setIsAnswering] = useState<boolean>(false);
  const [currentQuestion, setCurrentQuestion] = useState<
    NumericalQuestion | MultipleChoiceQuestion | TrueOrFalseQuestion | undefined
  >(undefined);
  const [questionList, setQuestionList] = useState<Question[] | undefined>(
    undefined
  );
  const [questionIndex, setQuestionIndex] = useState<string | undefined>(
    undefined
  );
  const [messageList, setMessageList] = useState<Array<Message>>([
    {
      messageContent: DEFAULT_MESSAGE,
      fromChatbot: true,
      question: undefined
    }
  ]);
  const [messageContent, setMessageContent] = useState<string>('');

  const updateMessageList = (response: ChatbotResponse) => {
    setIsAnswering(response.state.isAnswering);
    if (response.state.currentQuestion) {
      setCurrentQuestion(response.state.currentQuestion);
    }

    if (response.state.questionList) {
      setQuestionList(response.state.questionList);
    }

    if (response.state.questionIndex) {
      setQuestionIndex(response.state.questionIndex);
    }

    setMessageList([
      ...messageList,
      {
        messageContent: response.state.message,
        fromChatbot: true,
        question: response.state.currentQuestion
      }
    ]);
  };

  useEffect(() => {
    socket.connect();

    startDefaultListeners(socket);

    initialiseChatRoom(socket, updateMessageList);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [messageList]);

  const sendMessage = (messageContent: string) => {
    setMessageList([
      ...messageList,
      { messageContent, fromChatbot: false, question: undefined }
    ]);
    socket.emit('message', {
      username: 'test',
      room: '1',
      state: {
        message: messageContent,
        isAnswering,
        currentQuestion,
        questionList,
        questionIndex
      }
    });
  };

  const handleSendMessage = () => {
    if (messageContent !== '') {
      sendMessage(messageContent);
      setMessageContent('');
    }
  };

  const handleEnterSubmit = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && e.shiftKey === false) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <MainContainer current={Page.CHATROOM}>
      <div className="chatroom">
        <MessageList
          messageList={messageList}
          handleSendMessage={handleSendMessage}
          setMessageContent={setMessageContent}
        />
        <MessageBox
          handleSendMessage={handleSendMessage}
          messageContent={messageContent}
          setMessageContent={setMessageContent}
          handleEnterSubmit={handleEnterSubmit}
        />
      </div>
    </MainContainer>
  );
};

export default ChatRoom;
