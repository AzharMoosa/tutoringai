import { Socket } from 'socket.io-client';

export interface ChatbotResponse {
  message: string;
}

export const startDefaultListeners = (socket: Socket) => {
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

export const initialiseChatRoom = (
  socket: Socket,
  messageListener: (response: ChatbotResponse) => void
) => {
  socket.emit('join', { username: 'test', room: '1' });
  socket.on('recieved_message', messageListener);
};
