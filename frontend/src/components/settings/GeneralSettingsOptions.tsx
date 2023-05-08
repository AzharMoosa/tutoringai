import TextBoxSetting from './TextBoxSetting';
import './GeneralSettingsOptions.css';
import { useAppDispatch } from '../../hooks/redux/hooks';
import { useState } from 'react';
import {
  updateUser,
  UpdatedUserDetails,
  IUserDetails
} from '../../features/user/userSlice';

const GeneralSettingsOptions = ({
  userDetails
}: {
  userDetails: IUserDetails;
}) => {
  const dispatch = useAppDispatch();

  const [email, setEmail] = useState(userDetails.email);
  const [fullName, setFullName] = useState(userDetails.fullName);
  const [password, setPassword] = useState('');

  const updateUserDetails = () => {
    const updatedUserDetails: UpdatedUserDetails = {};

    if (password !== '') {
      updatedUserDetails.password = password;
    }

    if (fullName !== '') {
      updatedUserDetails.fullName = fullName;
    }

    dispatch(updateUser(updatedUserDetails));
  };

  return (
    <div className="general-settings-options">
      <TextBoxSetting
        label={'Email'}
        name={'email'}
        value={email}
        setValue={setEmail}
        disabled={true}
      />
      <TextBoxSetting
        label={'Full Name'}
        name={'fullName'}
        placeholder={'Full Name'}
        value={fullName}
        setValue={setFullName}
      />
      <TextBoxSetting
        label={'Password'}
        name={'password'}
        placeholder={'Password'}
        value={password}
        setValue={setPassword}
        type={'password'}
      />
      <button onClick={updateUserDetails} className="update-btn">
        Update
      </button>
    </div>
  );
};

export default GeneralSettingsOptions;
