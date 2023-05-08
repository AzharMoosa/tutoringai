import './TextBoxSetting.css';

interface TextBoxOptions {
  name: string;
  type?: string;
  placeholder?: string;
  value: string;
  disabled?: boolean;
  label: string;
  setValue: (value: string) => void;
}

const TextBoxSetting = ({
  name,
  placeholder = '',
  type = 'text',
  value,
  setValue,
  disabled = false,
  label
}: TextBoxOptions) => {
  return (
    <div className="input-container">
      <h4>{label}</h4>
      <input
        disabled={disabled}
        name={name}
        value={value}
        type={type}
        placeholder={placeholder}
        onChange={(e) => setValue(e.target.value)}
      />
    </div>
  );
};

export default TextBoxSetting;
