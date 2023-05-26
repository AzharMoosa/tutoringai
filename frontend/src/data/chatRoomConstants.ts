export const WEB_SOCKET_URI: string =
  !process.env.NODE_ENV || process.env.NODE_ENV === 'development'
    ? 'http://127.0.0.1:5000/'
    : 'https://chatbot-marc.herokuapp.com/';
export const WEB_SOCKET_CONFIG: any = {
  reconnectionAttempts: 5,
  reconnectionDelay: 5000,
  autoConnect: false
};
export const DEFAULT_MESSAGE: string = "Hello I'm M.A.R.C.";
