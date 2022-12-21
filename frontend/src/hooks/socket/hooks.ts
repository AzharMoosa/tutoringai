import io, { ManagerOptions, SocketOptions, Socket } from 'socket.io-client';
import { useEffect, useRef } from 'react';

export const useSocket = (
  uri: string,
  opts?: Partial<ManagerOptions & SocketOptions> | undefined
): Socket => {
  const { current: socket } = useRef(io(uri, opts));

  useEffect(() => {
    return () => {
      if (socket) socket.close();
    };
  }, [socket]);

  return socket;
};
