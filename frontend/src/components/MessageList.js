import React from 'react';
import './MessageList.css';
import Message from './Message';

const MessageList = ({ messages, loading }) => {
  return (
    <div className="message-list">
      {messages.map((message) => (
        <Message 
          key={message.id} 
          message={message}
        />
      ))}
      
      {loading && (
        <div className="loading-message">
          <div className="typing-indicator">
            <div className="typing-dot"></div>
            <div className="typing-dot"></div>
            <div className="typing-dot"></div>
          </div>
        </div>
      )}
    </div>
  );
};

export default MessageList; 