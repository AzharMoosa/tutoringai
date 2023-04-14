import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';
import API from '../../lib/api';
import toast from 'react-hot-toast';

export interface IUserDetails {
  email: string;
  fullName: string;
  _id: string;
  token: string;
}

interface UserState {
  userDetails: IUserDetails | null;
  loading: boolean;
  error: string | null;
}

const initialState: UserState = {
  userDetails: null,
  loading: true,
  error: null
};


export const getUser = createAsyncThunk(
  'get/user',
  async (thunkAPI) => {
    const token = localStorage.getItem('token');
    const config = {
      headers: { Authorization: `Bearer ${token}` }
    };
    const { data } = await API.get('/api/users', config);
    return data;
  }
);

export const UserSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder.addCase(getUser.fulfilled, (state, action) => {
      state.userDetails = action.payload;
      state.loading = false;
    });
    builder.addCase(getUser.rejected, (state, action) => {
      toast.error('Invalid Email or Password', { id: 'invalid-login' });
    });
  }
});


export default UserSlice.reducer;
