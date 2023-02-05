import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';
import API from '../../lib/api';
import toast from 'react-hot-toast';

export interface IAuthDetails {
  email: string;
  fullName: string;
  _id: string;
  token: string;
}

export interface ILoginDetails {
  email: string;
  password: string;
}

export interface IRegisterDetails {
  email: string;
  fullName: string;
  password: string;
}

interface AuthState {
  authDetails: IAuthDetails | null;
  token: string | null;
  error: string | null;
}

const initialState: AuthState = {
  authDetails: null,
  token: localStorage.getItem('token'),
  error: null
};

export const loginUser = createAsyncThunk(
  'login/user',
  async (loginDetails: ILoginDetails, thunkAPI) => {
    const { data } = await API.post('/api/auth/login', loginDetails);
    localStorage.setItem('token', data.token);
    return data;
  }
);

export const registerUser = createAsyncThunk(
  'register/user',
  async (registerDetails: IRegisterDetails, thunkAPI) => {
    const { data } = await API.post('/api/auth/register', registerDetails);
    localStorage.setItem('token', data.token);
    return data;
  }
);

export const AuthSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    logout: (state, action) => {
      state.authDetails = null;
      state.token = null;
    }
  },
  extraReducers: (builder) => {
    builder.addCase(loginUser.fulfilled, (state, action) => {
      state.authDetails = action.payload;
      state.token = action.payload.token;
    });
    builder.addCase(loginUser.rejected, (state, action) => {
      toast.error("Invalid Email or Password", { id: "invalid-login"});
    });
    builder.addCase(registerUser.fulfilled, (state, action) => {
      state.authDetails = action.payload;
      state.token = action.payload.token;
    });
    builder.addCase(registerUser.rejected, (state, action) => {
      toast.error("Unable to create new user", { id: "invalid-register"});
    });
  }
});

export const { logout } = AuthSlice.actions;

export default AuthSlice.reducer;
