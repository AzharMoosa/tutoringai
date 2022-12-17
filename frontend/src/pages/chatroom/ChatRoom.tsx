import React, { useState } from 'react';
import { io } from 'socket.io-client';
import './ChatRoom.css';
import MessageBox from '../../components/chatroom/MessageBox';
import MessageList from '../../components/chatroom/MessageList';
import { Message } from '../../components/chatroom/types';
import { sendUserMessage } from '../../features/chatroom/chatRoom';

const ChatRoom = () => {
  const socket = io('http://127.0.0.1:5000/');
  socket.emit('join', { username: 'test', room: '1' });
  const [messageList, setMessageList] = useState<Array<Message>>([
    { messageContent: 'Hello', fromChatbot: true },
    { messageContent: 'Hello', fromChatbot: false },
    { messageContent: 'Hello', fromChatbot: true }
  ]);

  const sendMessage = (messageContent: string) => {
    setMessageList([...messageList, { messageContent, fromChatbot: false }]);
    sendUserMessage();
  };

  return (
    <div className="chatroom">
      <MessageList messageList={messageList} />
      <MessageBox sendMessage={sendMessage} />
    </div>
  );
};

export default ChatRoom;
