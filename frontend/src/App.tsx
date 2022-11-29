import React, { useEffect, useState } from 'react';
import './assets/App.css';
import { io } from 'socket.io-client';

const App = () => {
  const socket = io('http://127.0.0.1:5000/');
  socket.emit('join', { username: 'test', room: '1' });
  return (
    <div>
      <h1>Chatbot</h1>
    </div>
  );
};

export default App;
