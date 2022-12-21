import React, { useState, useEffect } from 'react';
import './ChatRoom.css';
import MessageBox from '../../components/chatroom/MessageBox';
import MessageList from '../../components/chatroom/MessageList';
import { Message } from '../../components/chatroom/types';
import { useSocket } from '../../hooks/socket/hooks';

interface ChatbotResponse {
  message: string
}

const ChatRoom = () => {
  const socket = useSocket('http://127.0.0.1:5000/', {
    reconnectionAttempts: 5,
    reconnectionDelay: 5000,
    autoConnect: false
  });

  const [messageList, setMessageList] = useState<Array<Message>>([
    { messageContent: 'Hello I\'m M.A.R.C.', fromChatbot: true },
  ]);

  useEffect(() => {
    socket.connect();

    startDefaultListeners();

    socket.emit('join', { username: 'test', room: '1' });

    socket.on('recieved_message', (response: ChatbotResponse) => {
      setMessageList([
        ...messageList,
        { messageContent: response.message, fromChatbot: true }
      ]);
    });
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [messageList]);

  const startDefaultListeners = () => {
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

  const sendMessage = (messageContent: string) => {
    setMessageList([...messageList, { messageContent, fromChatbot: false }]);
    socket.emit('message', { username: 'test', message: messageContent, room: '1' });
  };

  return (
    <div className="chatroom">
      <MessageList messageList={messageList} />
      <MessageBox sendMessage={sendMessage} />
    </div>
  );
};

export default ChatRoom;
