import React, { useState } from 'react';
import './UserInput.css';

const UserInput = ({ value, onChange, onSend, loading }) => {
  const [inputValue, setInputValue] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (inputValue.trim() && !loading) {
      onSend(inputValue);
      setInputValue('');
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
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message here..."
            disabled={loading}
            rows="1"
          />
          <button 
            type="submit" 
            className="send-button"
            disabled={!inputValue.trim() || loading}
          >
            {loading ? '⏳' : '📤'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default UserInput; 