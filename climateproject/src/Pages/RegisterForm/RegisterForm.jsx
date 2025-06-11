import { useState } from 'react';
import { FcGoogle } from 'react-icons/fc';
import { FaGithub } from 'react-icons/fa';
import InputField from '../../Components/InputFeild';
import img from '../../assets/signupimage.jpg';
import '../../Styles/Register.css';
import logo from '../../assets/CoastalSevenlogo.png';
import { registerUser } from '../../api/registerApi';
import { Link } from 'react-router-dom';
const RegisterForm = () => {
  const [form, setForm] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
  });

  const [errors, setErrors] = useState({
    password: '',
    confirmPassword: '',
    terms: '',
  });

  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [agreeTerms, setAgreeTerms] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
    setErrors({ ...errors, [e.target.name]: '' });
  };

  const handleCheckboxChange = (e) => {
    setAgreeTerms(e.target.checked);
    setErrors({ ...errors, terms: '' });
  };

  const isPasswordValid = (password) => {
    const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$/;
    return passwordRegex.test(password);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    let valid = true;
    const newErrors = { password: '', confirmPassword: '', terms: '' };

    if (!agreeTerms) {
      newErrors.terms = 'Please agree to the Terms & Conditions';
      valid = false;
    }

    if (!isPasswordValid(form.password)) {
      newErrors.password =
        'Password must be at least 8 characters and include uppercase, lowercase, number, and special character.';
      valid = false;
    }

    if (form.password !== form.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match.';
      valid = false;
    }

    setErrors(newErrors);
    if (!valid) return;

    try {
      const response = await registerUser(form);
      console.log('User registered:', response);
      alert('Registration successful!');
      setForm({ name: '', email: '', password: '', confirmPassword: '' });
      setErrors({ password: '', confirmPassword: '', terms: '' });
      setShowPassword(false);
      setShowConfirmPassword(false);
      setAgreeTerms(false);
    } catch (err) {
      alert('Registration failed: ' + err.message);
    }
  };

  return (
    <div className="register-container">
      <div className="image-section">
        <img src={img} alt="illustration" />
      </div>

      <div className="form-section">
        <div className="logo-container">
          <img src={logo} alt="Company Logo" />
        </div>

        <h2>Create your account</h2>
        <p>Welcome to COASTALSEVEN TECHNOLOGIES</p>

        <div className="auth-buttons">
          <button className="google-btn"><FcGoogle /> Google</button>
          <button className="github-btn"><FaGithub /> GitHub</button>
        </div>

        <p className="divider">Or continue with</p>

        <form onSubmit={handleSubmit}>
          <InputField
            label="Name"
            type="text"
            name="name"
            placeholder="Enter name"
            value={form.name}
            onChange={handleChange}
          />

          <InputField
            label="Email id"
            type="email"
            name="email"
            placeholder="Enter email id"
            value={form.email}
            onChange={handleChange}
          />

          <div className="input-group">
            <InputField
              label="Password"
              type="password"
              name="password"
              placeholder="Enter password"
              value={form.password}
              onChange={handleChange}
              showPassword={showPassword}
              togglePasswordVisibility={() => setShowPassword(!showPassword)}
              className={errors.password ? 'error-input' : ''}
            />
            {errors.password && <span className="error-text">{errors.password}</span>}
          </div>

          <div className="input-group">
            <InputField
              label="Confirm Password"
              type="password"
              name="confirmPassword"
              placeholder="Enter confirm password"
              value={form.confirmPassword}
              onChange={handleChange}
              showPassword={showConfirmPassword}
              togglePasswordVisibility={() => setShowConfirmPassword(!showConfirmPassword)}
              className={errors.confirmPassword ? 'error-input' : ''}
            />
            {errors.confirmPassword && <span className="error-text">{errors.confirmPassword}</span>}
          </div>

          <div className="terms">
            <input
              type="checkbox"
              id="agree"
              checked={agreeTerms}
              onChange={handleCheckboxChange}
            />
            <label htmlFor="agree">I agree to the <a href="#">Terms & Conditions</a></label>
          </div>
          {errors.terms && <span className="error-text">{errors.terms}</span>}

          <button type="submit" className="signup-btn">Sign Up</button>
          <p className="signin-link">Already have an account? <Link to="/signin">Sign In</Link></p>
        </form>
      </div>
    </div>
  );
};

export default RegisterForm;