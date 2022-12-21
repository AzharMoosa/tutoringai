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
  initialiseChatRoom
} from '../../utils/chatRoomUtils';

const ChatRoom = () => {
  const socket = useSocket(WEB_SOCKET_URI, WEB_SOCKET_CONFIG);

  const [messageList, setMessageList] = useState<Array<Message>>([
    { messageContent: DEFAULT_MESSAGE, fromChatbot: true }
  ]);

  const updateMessageList = (response: ChatbotResponse) =>
    setMessageList([
      ...messageList,
      { messageContent: response.message, fromChatbot: true }
    ]);

  useEffect(() => {
    socket.connect();

    startDefaultListeners(socket);

    initialiseChatRoom(socket, updateMessageList);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [messageList]);

  const sendMessage = (messageContent: string) => {
    setMessageList([...messageList, { messageContent, fromChatbot: false }]);
    socket.emit('message', {
      username: 'test',
      message: messageContent,
      room: '1'
    });
  };

  return (
    <div className="chatroom">
      <MessageList messageList={messageList} />
      <MessageBox sendMessage={sendMessage} />
    </div>
  );
};

export default ChatRoom;
