import React, { useEffect } from 'react';
import './ConversationHistoryPanel.css';
import { useChat } from '../context/ChatContext';

const ConversationHistoryPanel = ({ isVisible, onLoadConversation, onClose }) => {
  const { state, actions } = useChat();
  const { conversations } = state;

  // Fetch conversations when panel is opened
  useEffect(() => {
    if (isVisible) {
      fetchConversations();
    }
  }, [isVisible]);

  const fetchConversations = async () => {
    try {
      // For demo purposes, we'll create some mock conversations
      // In a real app, you would fetch from the API
      const mockConversations = [
        {
          id: 'conv-1',
          title: 'Product Inquiry',
          created_at: new Date(Date.now() - 86400000).toISOString(), // 1 day ago
          message_count: 4
        },
        {
          id: 'conv-2',
          title: 'Order Status Check',
          created_at: new Date(Date.now() - 172800000).toISOString(), // 2 days ago
          message_count: 6
        },
        {
          id: 'conv-3',
          title: 'Inventory Question',
          created_at: new Date(Date.now() - 259200000).toISOString(), // 3 days ago
          message_count: 3
        }
      ];

      actions.setConversations(mockConversations);
    } catch (error) {
      console.error('Error fetching conversations:', error);
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 1) {
      return 'Yesterday';
    } else if (diffDays < 7) {
      return `${diffDays} days ago`;
    } else {
      return date.toLocaleDateString();
    }
  };

  const handleConversationClick = (conversationId) => {
    onLoadConversation(conversationId);
  };

  if (!isVisible) {
    return null;
  }

  return (
    <div className="conversation-history-panel">
      <div className="history-header">
        <h3>Conversation History</h3>
        <button className="close-button" onClick={onClose}>
          ✕
        </button>
      </div>

      <div className="history-content">
        {conversations.length === 0 ? (
          <div className="no-conversations">
            <p>No previous conversations found.</p>
            <p>Start a new chat to begin!</p>
          </div>
        ) : (
          <div className="conversation-list">
            {conversations.map((conversation) => (
              <div
                key={conversation.id}
                className="conversation-item"
                onClick={() => handleConversationClick(conversation.id)}
              >
                <div className="conversation-info">
                  <h4 className="conversation-title">{conversation.title}</h4>
                  <p className="conversation-date">
                    {formatDate(conversation.created_at)}
                  </p>
                  <p className="conversation-messages">
                    {conversation.message_count} messages
                  </p>
                </div>
                <div className="conversation-arrow">→</div>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="history-footer">
        <button className="refresh-button" onClick={fetchConversations}>
          🔄 Refresh
        </button>
      </div>
    </div>
  );
};

export default ConversationHistoryPanel; 