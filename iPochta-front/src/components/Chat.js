import React, { useState, useEffect } from 'react';
import '../css/styles.css';
import { fetchUsername } from '../api/user';

const Chat = ({ partner, chatHistory, onPartnerChange }) => {
  const [socket, setSocket] = useState(null);
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [selectedPartner, setSelectedPartner] = useState(partner || '');
  const [username, setUsername] = useState('');

  useEffect(() => {
    setSelectedPartner(partner);
  }, [partner]); 

  useEffect(() => {
    const getUsername = async () => {
      const fetchedUsername = await fetchUsername();
      if (fetchedUsername) {
        setUsername(fetchedUsername);
      }
    };
    
    getUsername();
  }, []);

  useEffect(() => {
    if (chatHistory) {
      const formattedHistory = chatHistory.map(msg => ({
        ...msg,
        sender_username: msg.sender_username === username ? 'me' : msg.sender_username,
      }));
      setMessages(formattedHistory);
    }
  }, [chatHistory, username]);

  useEffect(() => {
    if (selectedPartner) {
      const ws = new WebSocket(`ws://127.0.0.1:8000/ws/${selectedPartner}`);
      setSocket(ws);

      ws.onopen = () => {
        console.log("WebSocket connection opened with:", selectedPartner);
      };
      
      ws.onmessage = (event) => {
        const message = JSON.parse(event.data);
        console.log("Received message:", message);
        const formattedMessage = {
          ...message,
          sender_username: message.sender === username ? 'me' : message.sender,
        };
        setMessages((prevMessages) => [...prevMessages, formattedMessage]);
      };

      return () => {
        ws.close();
      };
    }
  }, [selectedPartner, username]);

  const handleSendMessage = () => {
    if (socket && newMessage) {
      socket.send(JSON.stringify({ recipient: selectedPartner, content: newMessage }));
      setMessages((prevMessages) => [
        ...prevMessages,
        { sender_username: 'me', content: newMessage, timestamp: new Date().toISOString() },
      ]);
      setNewMessage('');
    }
  };

  const handlePartnerInputChange = (e) => {
    const newPartner = e.target.value;
    setSelectedPartner(newPartner);
    onPartnerChange(newPartner);
};

  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="chat-container">
      <h3>Выберите собеседника:</h3>
      <div className="chat-input">
        <input
          value={selectedPartner}
          onChange={handlePartnerInputChange}
          placeholder="Введите имя пользователя"
        />
      </div>

      <div className="chat-messages">
        {messages.map((msg, index) => (
          <div
            key={msg.id || index}
            className={`chat-message ${
              msg.sender_username === 'me' ? 'sender' : 'recipient'
            }`}
          >
            <div className="message-content">
              <strong>{msg.sender_username}:</strong> {msg.content}
              <div className="timestamp">{formatTimestamp(msg.timestamp)}</div>
            </div>
          </div>
        ))}
      </div>

      <div className="chat-input">
        <input
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          placeholder="Ваше сообщение..."
        />
        <button onClick={handleSendMessage}>Отправить</button>
      </div>
    </div>
  );
};

export default Chat;
