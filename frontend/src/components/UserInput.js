import React from 'react';
import './UserInput.css';
import { useChat } from '../context/ChatContext';

const UserInput = ({ onSend, loading, disabled = false }) => {
  const { state, actions } = useChat();
  const { userInput } = state;

  const handleSubmit = (e) => {
    e.preventDefault();
    if (userInput.trim() && !loading && !disabled) {
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
        <div className={`input-wrapper ${disabled ? 'disabled' : ''}`}>
          <textarea
            className="message-input"
            value={userInput}
            onChange={(e) => actions.setUserInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder={disabled ? "Backend disconnected. Please check connection." : "Type your message here..."}
            disabled={loading || disabled}
            rows="1"
          />
          <button 
            type="submit" 
            className="send-button"
            disabled={!userInput.trim() || loading || disabled}
          >
            {loading ? '⏳' : disabled ? '❌' : '📤'}
          </button>
        </div>
        {disabled && (
          <div className="connection-warning">
            ⚠️ Backend service is not available. Please check if the server is running.
          </div>
        )}
      </form>
    </div>
  );
};

export default UserInput; 