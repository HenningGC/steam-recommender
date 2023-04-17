import React, { useState } from 'react';

const Chatbox = () => {
  const [userMessage, setUserMessage] = useState('');
  const [conversationHistory, setConversationHistory] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [input, setInput] = useState('');

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!userMessage) return;

    setIsLoading(true);
    setConversationHistory((prevHistory) => `${prevHistory}\nUser: ${userMessage}`);
    console.log(conversationHistory)
    try {
      const response = await fetch('http://127.0.0.1:5000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userMessage, history: conversationHistory }),
      });

      const data = await response.json();

      if (data.response) {
        setConversationHistory((prevHistory) => `${prevHistory}\nSystem: ${data.response}`);
      } else {
        setConversationHistory((prevHistory) => `${prevHistory}\nError: ${data.error}`);
      }
    } catch (error) {
      setConversationHistory((prevHistory) => `${prevHistory}\nError: Failed to fetch chat response.`);
    }

    setIsLoading(false);
    setUserMessage('');
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    sendMessage(event);
  };

  return (
    <div>
      <h2>Chatbot</h2>
      <div style={{ whiteSpace: 'pre-wrap', background: 'lightgray', minHeight: '200px', maxHeight: '400px', overflowY: 'auto' }}>
        {conversationHistory}
      </div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Type your message"
          value={userMessage}
          onChange={(e) => setUserMessage(e.target.value)} // Update userMessage state instead of input
        />
        <button type="submit" disabled={isLoading}>
          Send
        </button>
      </form>
    </div>
  );
};

export default Chatbox;
