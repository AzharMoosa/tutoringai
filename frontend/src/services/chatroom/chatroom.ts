import axios from 'axios';
import { IUserDetails } from '../../features/user/userSlice';
import toast from 'react-hot-toast';

export const initialiseChatroom = async (userDetails: IUserDetails | null) => {
  try {
    await axios.post('/api/chatbot/initialise', {
        username: `${userDetails?.fullName ?? 'unknown'}`,
        room: `${userDetails?._id ?? 'unknown'}`
      });
  } catch {
    toast.error('Server Error', { id: 'chatroom-initialise' });
  }
};

export const sendMessageToChatbot = async (data: any) => {
    const { data: response } = await axios.post('/api/chatbot', data);
    return response;
}