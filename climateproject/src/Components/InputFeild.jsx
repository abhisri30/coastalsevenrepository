import '../Styles/InputFeild.css';
import { FaEye, FaEyeSlash } from 'react-icons/fa';

const InputField = ({
  label,
  type = 'text',
  placeholder,
  value,
  onChange,
  name,
  showPassword,
  togglePasswordVisibility,
}) => {
  return (
    <div className="mb-4">
      <label className="block text-gray-700 mb-1">{label}</label>
      <div className="input-wrapper relative">
        <input
          type={showPassword && type === 'password' ? 'text' : type}
          placeholder={placeholder}
          value={value}
          name={name}
          onChange={onChange}
          className="input-field"
        />
        {type === 'password' && (
          <button
            type="button"
            onClick={togglePasswordVisibility}
            className="absolute inset-y-0 right-0 flex items-center pr-3"
          >
            {showPassword ? <FaEyeSlash /> : <FaEye />}
          </button>
        )}
      </div>
    </div>
  );
};

export default InputField;