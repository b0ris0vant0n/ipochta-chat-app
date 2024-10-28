import React, { useState } from 'react';
import { loginUser } from '../api/auth';
import { useNavigate } from 'react-router-dom';
import '../css/styles.css';


const LoginForm = () => {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
      username: '',
      password: '',
    });
    const [error, setError] = useState(null);
  
    const handleChange = (e) => {
      const { name, value } = e.target;
      console.log('Name:', name, 'Value:', value);
      setFormData((prevData) => ({ ...prevData, [name]: value }));
    };
  
    const handleSubmit = async (e) => {
      e.preventDefault();
      const loginResult = await loginUser(formData);
      console.log('login')
      if (loginResult.success) {
        console.log('Login successfully');
      localStorage.setItem("email", formData.username);
      console.log(localStorage.getItem("email"))

      navigate('/chat')
      } else {
        setError(loginResult.error);
      }
    };
  
    return (
      <form className="login-form" onSubmit={handleSubmit}>
        <label>
          Email:
          <input
            name="username"
            className="input-field-login-form"
            type="email"
            onChange={handleChange}
            required
          />
        </label>
        <br />
        <label>
          Пароль:
          <input
            name="password"
            className="input-field-login-form"
            type="password"
            onChange={handleChange}
            required
          />
        </label>
        <br />
        <button type="submit" className="submit-button-login-form">
          Логин
        </button>
        {error && <div className="error-message">{error}</div>}
      </form>
    );
  };
  
  export default LoginForm;
  