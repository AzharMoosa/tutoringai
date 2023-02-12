interface ButtonStyle {
  textContent: string;
  onClick?: any;
}

const Button = ({ textContent, onClick = () => {} }: ButtonStyle) => (
  <button onClick={onClick} className={`btn-primary`}>
    {textContent}
  </button>
);

export default Button;
