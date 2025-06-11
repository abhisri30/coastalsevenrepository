import { useState } from 'react';
import { FcGoogle } from 'react-icons/fc';
import { FaGithub } from 'react-icons/fa';
import InputField from '../../Components/InputFeild';
import logo from '../../assets/CoastalSevenlogo.png';
import signupImage from '../../assets/signupimage.jpg';
import '../../Styles/signupform.css';
import { Link } from 'react-router-dom';

const SignInForm = () => {
  const [form, setForm] = useState({
    email: '',
    password: '',
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevent default form submission

    try {
      const response = await fetch('/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(form),
      });

      const data = await response.json();

      if (response.ok) {
        console.log('Login successful:', data);
        // Navigate or store token, etc.
      } else {
        console.error('Login failed:', data.message);
      }
    } catch (error) {
      console.error('Error during login:', error);
    }
  };

  return (
    <div className="signup-wrapper">
      <div className="signup-image-side">
        <img src={signupImage} alt="Signup visual" className="signup-image" />
      </div>

      <div className="signup-form-side">
        <div className="signup-form-content">
          <div className="signup-logo-box">
            <img src={logo} alt="Company Logo" className="signup-logo" />
          </div>

          <h2 className="signup-heading">Sign In</h2>
          <p className="signup-subtext">Welcome back to COASTALSEVEN TECHNOLOGIES</p>

          <div className="signup-auth-buttons">
            <button className="signup-google-btn"><FcGoogle /> Continue with Google</button>
            <button className="signup-github-btn"><FaGithub /> Continue with GitHub</button>
          </div>

          <p className="signup-divider">Or continue with</p>

          <form className="signup-form" onSubmit={handleSubmit}>
            <InputField
              label="Email id"
              type="email"
              name="email"
              placeholder="Enter email id"
              value={form.email}
              onChange={handleChange}
            />

            <InputField
              label="Password"
              type="password"
              name="password"
              placeholder="Enter password"
              value={form.password}
              onChange={handleChange}
            />

            <button type="submit" className="signup-submit-btn">Sign In</button>
          </form>

          <p className="signup-login-link">
            Don’t have an account? <Link to="/register">Sign Up</Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default SignInForm;
