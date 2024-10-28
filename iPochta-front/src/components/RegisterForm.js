import React, { useState } from 'react';
import { registerUser } from '../api/auth';
import { useNavigate } from 'react-router-dom';
import '../css/styles.css';

const RegisterForm = ({ onRegister }) => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    username: '',
    telegram_username: ''
  });

  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({ ...prevData, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

  const registrationResult = await registerUser(formData);

    if (registrationResult.success) {
      navigate('/login');
    } else {
      setError(registrationResult.error);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="form-container">
      <input className="form-input" type="text" name="email" placeholder="Email" value={formData.email} onChange={handleChange} required />
      <input className="form-input" name="password" type="password" placeholder="Password" value={formData.password} onChange={handleChange} required />
      <input className="form-input" name="username" placeholder="Username" value={formData.username} onChange={handleChange} required />
      <input className="form-input" name="telegram_username" placeholder="Telegram Username" value={formData.telegram_username} onChange={handleChange} />
      <button type="submit">Зарегистрироваться</button>
      {error && <div className="error-message">{error}</div>}
    </form>
  );
};

export default RegisterForm;
