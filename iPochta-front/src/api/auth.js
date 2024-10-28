import axios from 'axios';


const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  withCredentials: true
});

export const loginUser = async (formData) => {
    try {
      const urlEncodedData = new URLSearchParams({
            grant_type: 'password',
            username: formData.username,
            password: formData.password,
            scope: '',
            client_id: '',
            client_secret: '',
          }).toString();
      
      const response = await fetch(`http://127.0.0.1:8000/auth/jwt/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: urlEncodedData,
        credentials: 'include',
      });
      console.log(response.status)
      if (response.ok) {
        return { success: true };
      } else {
        const errorData = await response.json();
        return { success: false, error: errorData.error };
      }
    } catch (error) {
      console.error('Error during login:', error);
      return { success: false, error: 'An unexpected error occurred during login.' };
    }
  };

  export const registerUser = async (formData) => {
    try {
      const requestData = {
          username: formData.username,
          password: formData.password,
          email: formData.email,
          telegram_username: formData.telegram_username,
          is_active: true,
          is_superuser: false,
          is_verified: false,
      };
  
      const response = await fetch(`http://127.0.0.1:8000/auth/register/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData),
      });
  
      if (!response.ok) {
        const errorData = await response.json();
        if (errorData.error) {
          return { success: false, error: errorData.error };
        } else {
          return { success: false, error: 'Произошла ошибка при регистрации' };
        }
      } else {
        console.log('User registered successfully');
        return { success: true };
      }
    } catch (error) {
      console.error('Error during registration:', error);
      return { success: false, error: 'An unexpected error occurred during registration.' };
    }
  };
  
export default registerUser;

export const logoutUser = async () => {
    await apiClient.post('/auth/jwt/logout');
    document.cookie = 'messaging=; Max-Age=0';
  };