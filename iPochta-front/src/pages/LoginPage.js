import React from 'react';
import LoginForm from '../components/LoginForm';
import { Link } from 'react-router-dom';
import '../css/styles.css';

const LoginPage = () => {
    return (
      <div className='login-container'>
        <h2>Вход</h2>
        <LoginForm />
        <p className='link-register'>
          Нет аккаунта? <Link to="/register">Зарегистрируйтесь</Link>
        </p>
      </div>
    );
  }

export default LoginPage;
