// API service for backend communication
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  // Generic request method
  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    
    const defaultOptions = {
      headers: {
        'Content-Type': 'application/json',
      },
      ...options,
    };

    try {
      const response = await fetch(url, defaultOptions);
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error(`API request failed for ${endpoint}:`, error);
      throw error;
    }
  }

  // Health check
  async healthCheck() {
    return this.request('/api/health');
  }

  // Chat endpoint
  async sendMessage(message, conversationId = null, userId = null) {
    const payload = {
      message,
      ...(conversationId && { conversation_id: conversationId }),
      ...(userId && { user_id: userId }),
    };

    return this.request('/api/chat', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  }

  // User management
  async createUser(userData) {
    return this.request('/api/users', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }

  // Conversation management
  async createConversation(userId, title = null) {
    return this.request('/api/conversations', {
      method: 'POST',
      body: JSON.stringify({
        user_id: userId,
        ...(title && { title }),
      }),
    });
  }

  async getConversation(conversationId) {
    return this.request(`/api/conversations/${conversationId}`);
  }

  async addMessage(conversationId, role, content) {
    return this.request(`/api/conversations/${conversationId}/messages`, {
      method: 'POST',
      body: JSON.stringify({
        role,
        content,
      }),
    });
  }

  async getUserConversations(userId) {
    return this.request(`/api/users/${userId}/conversations`);
  }

  // Database stats
  async getStats() {
    return this.request('/api/stats');
  }
}

// Create and export a singleton instance
const apiService = new ApiService();
export default apiService; 