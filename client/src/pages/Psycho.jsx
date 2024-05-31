import React, { useState, useEffect } from 'react';
import axios from 'axios';
import "./Psycho.css"; 
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";

function Psycho() {
  const [inputText, setInputText] = useState('');
  const [chatHistory, setChatHistory] = useState([{ sender: 'bot', text: "Hi, I am your therapist! How can I help you today?" }]);
  const [isSpeaking, setIsSpeaking] = useState(false);

  const toggleSpeakingMode = () => {
    setIsSpeaking(!isSpeaking);
  };

  const sendMessage = async () => {
    if (isSpeaking) return; // Don't send messages when in speaking mode

    if (inputText.trim() === '') return;
    const message = { text: inputText };
    try {
      const response = await axios.post('http://127.0.0.1:5000/chatbot', message);
      const audioUrl = response.data.audio_file_url + `?t=${new Date().getTime()}`;
      const audio = new Audio(audioUrl);
      audio.play();

      setChatHistory([
        ...chatHistory,
        { sender: 'user', text: inputText },
        { sender: 'bot', text: response.data.text },
      ]);
      setInputText('');
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  return (
    <div className="psycho-container">
      <Navbar />
      <div className="chat-container">
        <div className="chat-history">
          {chatHistory.map((message, index) => (
            <React.Fragment key={index}>
              {message.sender === 'user' ? (
                <div className="message user">{message.text}</div>
              ) : (
                <div className="message bot">{message.text}</div>
              )}
            </React.Fragment>
          ))}
            <div id="anchor"></div>

        </div>
      </div>
      <div className="input-container">
        <div className="input-box">
          <button onClick={toggleSpeakingMode}>
            {isSpeaking ? 'Stop Speaking' : 'Start Speaking'}
          </button>
          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Type your message here..."
            disabled={isSpeaking} // Disable input when in speaking mode
          />
          <button onClick={sendMessage} disabled={isSpeaking}>
            Send
          </button>
        </div>
      </div>
      <Footer />
    </div>
  );
}

export default Psycho;
