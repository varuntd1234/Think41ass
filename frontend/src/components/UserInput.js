import React from 'react';
import './UserInput.css';
import { useChat } from '../context/ChatContext';

const UserInput = ({ onSend, loading }) => {
  const { state, actions } = useChat();
  const { userInput } = state;

  const handleSubmit = (e) => {
    e.preventDefault();
    if (userInput.trim() && !loading) {
      onSend(userInput);
      actions.setUserInput('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="user-input-container">
      <form onSubmit={handleSubmit} className="user-input-form">
        <div className="input-wrapper">
          <textarea
            className="message-input"
            value={userInput}
            onChange={(e) => actions.setUserInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message here..."
            disabled={loading}
            rows="1"
          />
          <button 
            type="submit" 
            className="send-button"
            disabled={!userInput.trim() || loading}
          >
            {loading ? '⏳' : '📤'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default UserInput; 