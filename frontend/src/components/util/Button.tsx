import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faArrowRight } from '@fortawesome/free-solid-svg-icons';

interface ButtonStyle {
  textContent: string;
  primary?: boolean;
  icon?: string;
  small?: boolean;
}

const Button = ({ textContent, primary = true, icon, small }: ButtonStyle) => {
  return (
    <>
      {small ? (
        <button className="btn-small">{textContent}</button>
      ) : (
        <button className={`${primary ? 'btn-primary' : 'btn-secondary'}`}>
          {textContent}
          {icon && <FontAwesomeIcon icon={faArrowRight} />}
        </button>
      )}
    </>
  );
};

export default Button;
