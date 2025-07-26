import React, { createContext, useContext, useReducer } from 'react';

// Initial state
const initialState = {
  messages: [],
  loading: false,
  userInput: '',
  conversationId: null,
  conversations: [],
  showHistoryPanel: false
};

// Action types
const ACTIONS = {
  SET_MESSAGES: 'SET_MESSAGES',
  ADD_MESSAGE: 'ADD_MESSAGE',
  SET_LOADING: 'SET_LOADING',
  SET_USER_INPUT: 'SET_USER_INPUT',
  SET_CONVERSATION_ID: 'SET_CONVERSATION_ID',
  SET_CONVERSATIONS: 'SET_CONVERSATIONS',
  SET_HISTORY_PANEL: 'SET_HISTORY_PANEL',
  CLEAR_MESSAGES: 'CLEAR_MESSAGES',
  RESET_STATE: 'RESET_STATE'
};

// Reducer function
const chatReducer = (state, action) => {
  switch (action.type) {
    case ACTIONS.SET_MESSAGES:
      return {
        ...state,
        messages: action.payload
      };
    
    case ACTIONS.ADD_MESSAGE:
      return {
        ...state,
        messages: [...state.messages, action.payload]
      };
    
    case ACTIONS.SET_LOADING:
      return {
        ...state,
        loading: action.payload
      };
    
    case ACTIONS.SET_USER_INPUT:
      return {
        ...state,
        userInput: action.payload
      };
    
    case ACTIONS.SET_CONVERSATION_ID:
      return {
        ...state,
        conversationId: action.payload
      };
    
    case ACTIONS.SET_CONVERSATIONS:
      return {
        ...state,
        conversations: action.payload
      };
    
    case ACTIONS.SET_HISTORY_PANEL:
      return {
        ...state,
        showHistoryPanel: action.payload
      };
    
    case ACTIONS.CLEAR_MESSAGES:
      return {
        ...state,
        messages: []
      };
    
    case ACTIONS.RESET_STATE:
      return {
        ...initialState,
        messages: [
          {
            id: 'welcome',
            role: 'assistant',
            content: 'Hello! I\'m your AI assistant. I can help you with:\n\n• Product information and top sellers\n• Order status tracking\n• Inventory and stock levels\n• General e-commerce questions\n\nHow can I help you today?',
            timestamp: new Date().toISOString()
          }
        ]
      };
    
    default:
      return state;
  }
};

// Create context
const ChatContext = createContext();

// Provider component
export const ChatProvider = ({ children }) => {
  const [state, dispatch] = useReducer(chatReducer, initialState);

  // Action creators
  const actions = {
    setMessages: (messages) => {
      dispatch({ type: ACTIONS.SET_MESSAGES, payload: messages });
    },
    
    addMessage: (message) => {
      dispatch({ type: ACTIONS.ADD_MESSAGE, payload: message });
    },
    
    setLoading: (loading) => {
      dispatch({ type: ACTIONS.SET_LOADING, payload: loading });
    },
    
    setUserInput: (input) => {
      dispatch({ type: ACTIONS.SET_USER_INPUT, payload: input });
    },
    
    setConversationId: (id) => {
      dispatch({ type: ACTIONS.SET_CONVERSATION_ID, payload: id });
    },
    
    setConversations: (conversations) => {
      dispatch({ type: ACTIONS.SET_CONVERSATIONS, payload: conversations });
    },
    
    setHistoryPanel: (show) => {
      dispatch({ type: ACTIONS.SET_HISTORY_PANEL, payload: show });
    },
    
    clearMessages: () => {
      dispatch({ type: ACTIONS.CLEAR_MESSAGES });
    },
    
    resetState: () => {
      dispatch({ type: ACTIONS.RESET_STATE });
    }
  };

  return (
    <ChatContext.Provider value={{ state, actions }}>
      {children}
    </ChatContext.Provider>
  );
};

// Custom hook to use the context
export const useChat = () => {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error('useChat must be used within a ChatProvider');
  }
  return context;
}; 