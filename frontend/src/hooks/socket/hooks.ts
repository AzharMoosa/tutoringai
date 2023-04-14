import io, { ManagerOptions, SocketOptions, Socket } from 'socket.io-client';
import { useEffect, useRef } from 'react';
import { useAppSelector } from '../../hooks/redux/hooks';

export const useSocket = (
  uri: string,
  opts?: Partial<ManagerOptions & SocketOptions> | undefined
): Socket => {
  const { current: socket } = useRef(io(uri, opts));
  const userDetails = useAppSelector((state) => state.user.userDetails);

  useEffect(() => {
    return () => {
      if (socket) {
        socket.emit('leave', {
          username: `${userDetails?.fullName ?? 'unknown'}`,
          room: `${userDetails?._id ?? 'unknown'}`,
        });
        socket.close();
      }
    };
  }, [socket, userDetails?._id, userDetails?.fullName]);

  return socket;
};
