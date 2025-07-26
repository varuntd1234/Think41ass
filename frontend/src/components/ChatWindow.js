import React, { useEffect, useState } from 'react';
import './ChatWindow.css';
import MessageList from './MessageList';
import UserInput from './UserInput';
import ConversationHistoryPanel from './ConversationHistoryPanel';
import { useChat } from '../context/ChatContext';
import apiService from '../services/api';

const ChatWindow = () => {
  const { state, actions } = useChat();
  const { 
    messages, 
    loading, 
    userInput, 
    conversationId, 
    conversations, 
    showHistoryPanel 
  } = state;

  const [connectionStatus, setConnectionStatus] = useState('checking');

  // Check backend connection on component mount
  useEffect(() => {
    checkBackendConnection();
  }, []);

  // Initialize with welcome message
  useEffect(() => {
    if (messages.length === 0) {
      actions.resetState();
    }
  }, []);

  const checkBackendConnection = async () => {
    try {
      await apiService.healthCheck();
      setConnectionStatus('connected');
    } catch (error) {
      console.error('Backend connection failed:', error);
      setConnectionStatus('disconnected');
    }
  };

  const handleSendMessage = async (message) => {
    if (!message.trim()) return;

    // Add user message to the list
    const userMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: message,
      timestamp: new Date().toISOString()
    };

    actions.addMessage(userMessage);
    actions.setUserInput('');
    actions.setLoading(true);

    try {
      // Use API service to send message
      const response = await apiService.sendMessage(message, conversationId);
      
      // Add AI response to the list
      const aiMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.ai_response || response.message,
        timestamp: response.timestamp || new Date().toISOString()
      };

      actions.addMessage(aiMessage);
      
      // Update conversation ID if this is a new conversation
      if (!conversationId && response.conversation_id) {
        actions.setConversationId(response.conversation_id);
      }

      // Update connection status on successful request
      setConnectionStatus('connected');
      
    } catch (error) {
      console.error('Error sending message:', error);
      
      // Handle different types of errors
      let errorMessage = 'Sorry, I encountered an error. Please try again.';
      
      if (error.message.includes('Failed to fetch')) {
        errorMessage = 'Unable to connect to the server. Please check your connection.';
        setConnectionStatus('disconnected');
      } else if (error.message.includes('500')) {
        errorMessage = 'Server error. Please try again later.';
      } else if (error.message.includes('400')) {
        errorMessage = 'Invalid request. Please check your message.';
      }

      const errorResponse = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: errorMessage,
        timestamp: new Date().toISOString()
      };
      actions.addMessage(errorResponse);
    } finally {
      actions.setLoading(false);
    }
  };

  const handleLoadConversation = async (conversationId) => {
    try {
      const response = await apiService.getConversation(conversationId);
      
      if (response.messages) {
        actions.setMessages(response.messages);
        actions.setConversationId(conversationId);
        actions.setHistoryPanel(false);
        setConnectionStatus('connected');
      }
    } catch (error) {
      console.error('Error loading conversation:', error);
      
      const errorMessage = {
        id: Date.now().toString(),
        role: 'assistant',
        content: 'Unable to load conversation. Please try again.',
        timestamp: new Date().toISOString()
      };
      actions.addMessage(errorMessage);
    }
  };

  const handleNewConversation = () => {
    actions.resetState();
    actions.setConversationId(null);
    actions.setHistoryPanel(false);
  };

  const getConnectionStatusColor = () => {
    switch (connectionStatus) {
      case 'connected':
        return '#28a745';
      case 'disconnected':
        return '#dc3545';
      default:
        return '#ffc107';
    }
  };

  const getConnectionStatusText = () => {
    switch (connectionStatus) {
      case 'connected':
        return 'Connected';
      case 'disconnected':
        return 'Disconnected';
      default:
        return 'Checking...';
    }
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
            <div className="connection-status" style={{ color: getConnectionStatusColor() }}>
              <span className="status-dot" style={{ backgroundColor: getConnectionStatusColor() }}></span>
              {getConnectionStatusText()}
            </div>
            <button 
              className="history-toggle"
              onClick={() => actions.setHistoryPanel(!showHistoryPanel)}
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
          onClose={() => actions.setHistoryPanel(false)}
        />
        
        <div className="chat-main">
          <MessageList 
            messages={messages} 
            loading={loading}
          />
          <UserInput 
            onSend={handleSendMessage}
            loading={loading}
            disabled={connectionStatus === 'disconnected'}
          />
        </div>
      </div>
    </div>
  );
};

export default ChatWindow; 