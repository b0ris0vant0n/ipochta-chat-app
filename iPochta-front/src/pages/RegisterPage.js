import React from 'react';
import RegisterForm from '../components/RegisterForm';
import { Link } from 'react-router-dom';
import '../css/styles.css';

export const RegisterPage = () => {
    return (
        <div className='registration-container'>
          <h2>Регистрация</h2>
          <RegisterForm />
          <p className='link-register'>
            Есть аккаунт? <Link to="/login">Логин</Link>
          </p>
        </div>
      );
    }

export default RegisterPage;
