import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getPartners, getChatHistory } from '../api/messaging';
import { logoutUser } from '../api/auth.js'
import PartnersList from '../components/PartnersList';
import Chat from '../components/Chat';

export const ChatPage = () => {
  const [partners, setPartners] = useState([]);
  const [selectedPartner, setSelectedPartner] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [isCheckingAuth, setIsCheckingAuth] = useState(true); 
  const email = localStorage.getItem("email");
  const username = localStorage.getItem("username")
  const navigate = useNavigate();

  useEffect(() => {
    if (!email) {
        navigate('/login');
    } else {
        setIsCheckingAuth(false);
        const fetchPartners = async () => {
          try {
            const partnersData = await getPartners();
            console.log("Partners data:", partnersData);
            setPartners(partnersData);
            
          } catch (error) {
            console.error('Error fetching partners:', error);
            alert('Ошибка при загрузке партнеров. Попробуйте позже.');
          }
        };
  
        fetchPartners();
      }
    }, [email, navigate]);

  const handleSelectPartner = async (partner) => {
    console.log("Selected partner:", partner);
    setSelectedPartner(typeof partner === 'string' ? partner : partner.username);

    try {
      const history = await getChatHistory(partner.username || partner);
      setChatHistory(history);
    } catch (error) {
      console.error('Error fetching chat history:', error);
      alert('Ошибка при загрузке истории чата. Попробуйте позже.');
    }
  };

  const handleLogout = async () => {
    try {
      await logoutUser(); 
      localStorage.removeItem("username");
      navigate('/login');
    } catch (error) {
      console.error('Ошибка при выходе из системы:', error);
      alert('Ошибка при выходе из системы. Попробуйте еще раз.');
    }
  };

  if (isCheckingAuth) {
    return <div>Загрузка...</div>;
  }

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1>Чат пользователя {email}</h1>
        <button onClick={handleLogout} className="logout-button">Logout</button>
      </div>

      <div style={{ display: 'flex' }}>
        <PartnersList partners={partners} onSelectPartner={handleSelectPartner} />
        <Chat partner={selectedPartner} chatHistory={chatHistory} onPartnerChange={setSelectedPartner} />
      </div>
    </div>
  );
};

export default ChatPage;
