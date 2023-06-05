import { useState, useEffect } from 'react';
import './ChatRoom.css';
import { useAppDispatch, useAppSelector } from '../../hooks/redux/hooks';
import { getUser } from '../../features/user/userSlice';

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
  const userDetails = useAppSelector((state) => state.user.userDetails);
  const loading = useAppSelector((state) => state.user.loading);

  const dispatch = useAppDispatch();

  useEffect(() => {
    dispatch(getUser());
  }, [dispatch, loading]);

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
  const [correctAnswers, setCorrectAnswers] = useState<string | undefined>(
    undefined
  );
  const [mode, setMode] = useState<string | undefined>(undefined);
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

    if (response.state.mode) {
      setMode(response.state.mode);
    }

    if (response.state.correctAnswers) {
      setCorrectAnswers(response.state.correctAnswers);
    }

    setMessageList((prevMessageList) => {
      const lastMessageIndex = prevMessageList.length - 1;
      const updatedLastMessage = {
        ...prevMessageList[lastMessageIndex],
        messageContent: response.state.message,
        fromChatbot: true,
        question: response.state.currentQuestion
      };

      return [
        ...prevMessageList.slice(0, lastMessageIndex),
        updatedLastMessage
      ];
    });
  };

  useEffect(() => {
    socket.connect();

    startDefaultListeners(socket);

    if (!loading) {
      initialiseChatRoom(socket, updateMessageList, userDetails);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [messageList, userDetails]);

  const sendMessage = (messageContent: string) => {
    setMessageList([
      ...messageList,
      { messageContent, fromChatbot: false, question: undefined },
      { messageContent: '', fromChatbot: true, question: undefined }
    ]);
    socket.emit('message', {
      username: `${userDetails?.fullName ?? 'unknown'}`,
      room: `${userDetails?._id ?? 'unknown'}`,
      state: {
        message: messageContent,
        isAnswering,
        currentQuestion,
        questionList,
        questionIndex,
        mode,
        correctAnswers
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
          setMessageContent={setMessageContent}
        />
        <MessageBox
          handleSendMessage={handleSendMessage}
          messageContent={messageContent}
          setMessageContent={setMessageContent}
          handleEnterSubmit={handleEnterSubmit}
          currentQuestion={currentQuestion}
        />
      </div>
    </MainContainer>
  );
};

export default ChatRoom;
