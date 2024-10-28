import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  withCredentials: true
});

export const getPartners = async () => {
    const response = await apiClient.get('/messaging/partners');
    console.log("Response data:", response.data);
    return response.data;
  };


export const getChatHistory = async (username) => {
  const response = await apiClient.get(`messaging/messages/history/${username}`);
  return response.data;
};

