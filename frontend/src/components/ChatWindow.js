import React, { useState, useEffect } from 'react';
import './ChatWindow.css';
import MessageList from './MessageList';
import UserInput from './UserInput';
import ConversationHistoryPanel from './ConversationHistoryPanel';

const ChatWindow = () => {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [userInput, setUserInput] = useState('');
  const [conversationId, setConversationId] = useState(null);
  const [conversations, setConversations] = useState([]);
  const [showHistoryPanel, setShowHistoryPanel] = useState(false);

  // Initialize with welcome message
  useEffect(() => {
    setMessages([
      {
        id: 'welcome',
        role: 'assistant',
        content: 'Hello! I\'m your AI assistant. I can help you with:\n\n• Product information and top sellers\n• Order status tracking\n• Inventory and stock levels\n• General e-commerce questions\n\nHow can I help you today?',
        timestamp: new Date().toISOString()
      }
    ]);
  }, []);

  const handleSendMessage = async (message) => {
    if (!message.trim()) return;

    // Add user message to the list
    const userMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: message,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setUserInput('');
    setLoading(true);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: message,
          conversation_id: conversationId
        })
      });

      const data = await response.json();

      if (response.ok) {
        // Add AI response to the list
        const aiMessage = {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content: data.ai_response,
          timestamp: data.timestamp
        };

        setMessages(prev => [...prev, aiMessage]);
        
        // Update conversation ID if this is a new conversation
        if (!conversationId && data.conversation_id) {
          setConversationId(data.conversation_id);
        }
      } else {
        // Handle error
        const errorMessage = {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content: 'Sorry, I encountered an error. Please try again.',
          timestamp: new Date().toISOString()
        };
        setMessages(prev => [...prev, errorMessage]);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleLoadConversation = async (conversationId) => {
    try {
      const response = await fetch(`/api/conversations/${conversationId}`);
      const data = await response.json();

      if (response.ok) {
        setMessages(data.messages);
        setConversationId(conversationId);
        setShowHistoryPanel(false);
      }
    } catch (error) {
      console.error('Error loading conversation:', error);
    }
  };

  const handleNewConversation = () => {
    setMessages([
      {
        id: 'welcome',
        role: 'assistant',
        content: 'Hello! I\'m your AI assistant. How can I help you today?',
        timestamp: new Date().toISOString()
      }
    ]);
    setConversationId(null);
    setShowHistoryPanel(false);
  };

  return (
    <div className="chat-window">
      <header className="chat-header">
        <div className="header-content">
          <div className="logo">
            <span className="logo-icon">🤖</span>
            <h1>Conversational AI</h1>
          </div>
          <div className="header-actions">
            <button 
              className="history-toggle"
              onClick={() => setShowHistoryPanel(!showHistoryPanel)}
            >
              📚 History
            </button>
            <button 
              className="new-chat"
              onClick={handleNewConversation}
            >
              ➕ New Chat
            </button>
          </div>
        </div>
      </header>

      <div className="chat-container">
        <ConversationHistoryPanel 
          isVisible={showHistoryPanel}
          conversations={conversations}
          onLoadConversation={handleLoadConversation}
          onClose={() => setShowHistoryPanel(false)}
        />
        
        <div className="chat-main">
          <MessageList 
            messages={messages} 
            loading={loading}
          />
          <UserInput 
            value={userInput}
            onChange={setUserInput}
            onSend={handleSendMessage}
            loading={loading}
          />
        </div>
      </div>
    </div>
  );
};

export default ChatWindow; 