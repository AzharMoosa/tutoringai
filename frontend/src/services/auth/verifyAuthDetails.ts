import toast from 'react-hot-toast';

export const isRegisterDetailsValid = (
  fullName: string,
  email: string,
  password: string,
  confirmPassword: string
): Boolean => {
  if (!(fullName && email && password && confirmPassword)) {
    toast.error('Please fill in all details.');
    return false;
  }

  if (password !== confirmPassword) {
    toast.error('Passwords do not match.');
    return false;
  }

  if (password.length < 8) {
    toast.error('Password must be greater than 8 characters.');
    return false;
  }

  return true;
};

export const isLoginDetailsValid = (
  email: string,
  password: string,
): Boolean => {
  if (!(email && password)) {
    toast.error('Please fill in all details.');
    return false;
  }

  return true;
};

