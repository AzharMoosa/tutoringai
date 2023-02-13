interface InputStyle {
  name: string;
  placeholder?: string;
  value: string;
  type: string;
  setValue: (value: string) => void;
}

const Input = ({
  name,
  value,
  type,
  placeholder = '',
  setValue
}: InputStyle) => (
  <input
    className="input-container"
    name={name}
    type={type}
    placeholder={placeholder}
    value={value}
    onChange={(e) => setValue(e.target.value)}
  />
);

export default Input;
