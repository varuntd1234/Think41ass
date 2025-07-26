import React, { useEffect } from 'react';
import './ChatWindow.css';
import MessageList from './MessageList';
import UserInput from './UserInput';
import ConversationHistoryPanel from './ConversationHistoryPanel';
import { useChat } from '../context/ChatContext';

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

  // Initialize with welcome message
  useEffect(() => {
    if (messages.length === 0) {
      actions.resetState();
    }
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

    actions.addMessage(userMessage);
    actions.setUserInput('');
    actions.setLoading(true);

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

        actions.addMessage(aiMessage);
        
        // Update conversation ID if this is a new conversation
        if (!conversationId && data.conversation_id) {
          actions.setConversationId(data.conversation_id);
        }
      } else {
        // Handle error
        const errorMessage = {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content: 'Sorry, I encountered an error. Please try again.',
          timestamp: new Date().toISOString()
        };
        actions.addMessage(errorMessage);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toISOString()
      };
      actions.addMessage(errorMessage);
    } finally {
      actions.setLoading(false);
    }
  };

  const handleLoadConversation = async (conversationId) => {
    try {
      const response = await fetch(`/api/conversations/${conversationId}`);
      const data = await response.json();

      if (response.ok) {
        actions.setMessages(data.messages);
        actions.setConversationId(conversationId);
        actions.setHistoryPanel(false);
      }
    } catch (error) {
      console.error('Error loading conversation:', error);
    }
  };

  const handleNewConversation = () => {
    actions.resetState();
    actions.setConversationId(null);
    actions.setHistoryPanel(false);
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
            value={userInput}
            onChange={actions.setUserInput}
            onSend={handleSendMessage}
            loading={loading}
          />
        </div>
      </div>
    </div>
  );
};

export default ChatWindow; 