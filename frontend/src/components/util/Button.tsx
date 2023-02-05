import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faArrowRight } from '@fortawesome/free-solid-svg-icons';

interface ButtonStyle {
  textContent: string;
  primary?: boolean;
  icon?: string;
  small?: boolean;
  onClick?: any;
}

const Button = ({
  textContent,
  primary = true,
  icon,
  small,
  onClick = () => {}
}: ButtonStyle) => {
  return (
    <>
      {small ? (
        <button className="btn-small" onClick={onClick}>
          {textContent}
        </button>
      ) : (
        <button
          onClick={onClick}
          className={`${primary ? 'btn-primary' : 'btn-secondary'}`}
        >
          {textContent}
          {icon && <FontAwesomeIcon icon={faArrowRight} />}
        </button>
      )}
    </>
  );
};

export default Button;
