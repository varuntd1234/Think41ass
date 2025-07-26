# Conversational AI Frontend

A modern React application for the Conversational AI Backend Service, featuring a chat interface with conversation history management.

## 🚀 Features

### **Core Chat Interface**
- **Real-time Messaging**: Send and receive messages with the AI assistant
- **Message Differentiation**: Clear visual distinction between user and AI messages
- **Loading States**: Typing indicators and loading animations
- **Responsive Design**: Works seamlessly on desktop and mobile devices

### **State Management**
- **React Context API**: Centralized state management using Context and useReducer
- **Persistent State**: Maintains conversation state across component updates
- **Loading Indicators**: Real-time loading status for better UX
- **Input Management**: Controlled form inputs with validation

### **Conversation History**
- **History Panel**: Side panel displaying past conversations
- **Conversation Loading**: Click to load previous conversation history
- **New Chat**: Start fresh conversations with reset functionality
- **Conversation Metadata**: Shows titles, dates, and message counts

## 🛠️ Technology Stack

- **React 18**: Latest React with hooks and modern patterns
- **Context API**: Built-in React state management
- **CSS3**: Modern styling with gradients and animations
- **Fetch API**: HTTP requests to backend service
- **Responsive Design**: Mobile-first approach

## 📁 Project Structure

```
frontend/
├── public/
│   └── index.html              # Main HTML file
├── src/
│   ├── components/
│   │   ├── ChatWindow.js       # Main chat container
│   │   ├── ChatWindow.css      # Chat window styles
│   │   ├── MessageList.js      # Message list component
│   │   ├── MessageList.css     # Message list styles
│   │   ├── Message.js          # Individual message component
│   │   ├── Message.css         # Message styles
│   │   ├── UserInput.js        # Input form component
│   │   ├── UserInput.css       # Input styles
│   │   ├── ConversationHistoryPanel.js  # History panel
│   │   └── ConversationHistoryPanel.css # History styles
│   ├── context/
│   │   └── ChatContext.js      # State management context
│   ├── App.js                  # Main app component
│   ├── App.css                 # App styles
│   ├── index.js                # React entry point
│   └── index.css               # Global styles
├── package.json                # Dependencies and scripts
└── README.md                   # This file
```

## 🎯 Components Overview

### **ChatWindow**
- **Primary Container**: Orchestrates the entire chat interface
- **State Management**: Integrates with ChatContext for state handling
- **API Integration**: Handles communication with backend service
- **Layout Management**: Responsive layout with history panel

### **MessageList**
- **Message Rendering**: Displays list of messages with proper ordering
- **Loading States**: Shows typing indicators during AI responses
- **Scroll Management**: Auto-scrolls to latest messages
- **Animation**: Smooth fade-in animations for new messages

### **Message**
- **Message Display**: Renders individual messages with proper styling
- **Role Differentiation**: Different styles for user vs AI messages
- **Timestamp Display**: Shows message timestamps
- **Content Formatting**: Handles multi-line text and formatting

### **UserInput**
- **Controlled Form**: Manages input state with validation
- **Submit Handling**: Handles form submission and Enter key presses
- **Loading States**: Disables input during message processing
- **Auto-resize**: Textarea that grows with content

### **ConversationHistoryPanel**
- **History Display**: Shows list of past conversations
- **Conversation Loading**: Enables loading previous conversations
- **Metadata Display**: Shows conversation titles, dates, and message counts
- **Refresh Functionality**: Allows refreshing conversation list

## 🔧 State Management

### **ChatContext Structure**
```javascript
{
  messages: [],           // Array of message objects
  loading: false,         // Loading state indicator
  userInput: '',          // Current input value
  conversationId: null,   // Current conversation ID
  conversations: [],      // List of past conversations
  showHistoryPanel: false // History panel visibility
}
```

### **Actions Available**
- `setMessages()`: Set entire message list
- `addMessage()`: Add single message
- `setLoading()`: Update loading state
- `setUserInput()`: Update input value
- `setConversationId()`: Set current conversation
- `setConversations()`: Update conversation list
- `setHistoryPanel()`: Toggle history panel
- `resetState()`: Reset to initial state

## 🚀 Getting Started

### **Prerequisites**
- Node.js (v14 or higher)
- npm or yarn
- Backend service running on localhost:5000

### **Installation**
```bash
cd frontend
npm install
```

### **Development**
```bash
npm start
```
The app will open at `http://localhost:3000`

### **Build for Production**
```bash
npm run build
```

## 🔌 API Integration

### **Backend Endpoints Used**
- `POST /api/chat`: Send messages and receive AI responses
- `GET /api/conversations/:id`: Load conversation history
- `GET /api/health`: Health check (for connection status)

### **Request Format**
```javascript
{
  message: "User message",
  conversation_id: "optional-conversation-id"
}
```

### **Response Format**
```javascript
{
  conversation_id: "conversation-id",
  user_message: "original message",
  ai_response: "AI response",
  timestamp: "2023-01-01T00:00:00.000Z"
}
```

## 🎨 Design Features

### **Visual Design**
- **Gradient Backgrounds**: Modern purple gradient theme
- **Smooth Animations**: Fade-in effects and hover animations
- **Responsive Layout**: Adapts to different screen sizes
- **Clean Typography**: Modern font stack with proper hierarchy

### **User Experience**
- **Real-time Feedback**: Immediate visual feedback for user actions
- **Loading States**: Clear indication of processing states
- **Error Handling**: Graceful error messages and recovery
- **Accessibility**: Proper ARIA labels and keyboard navigation

## 📱 Responsive Design

### **Breakpoints**
- **Desktop**: 1200px and above
- **Tablet**: 768px - 1199px
- **Mobile**: Below 768px

### **Mobile Features**
- **Touch-friendly**: Large touch targets for mobile devices
- **Optimized Layout**: Stacked layout for smaller screens
- **Keyboard Handling**: Proper mobile keyboard behavior
- **Performance**: Optimized for mobile performance

## 🔧 Configuration

### **Environment Variables**
The app uses a proxy configuration in `package.json` to forward API requests to the backend:
```json
{
  "proxy": "http://localhost:5000"
}
```

### **Customization**
- **Colors**: Modify CSS custom properties in component files
- **Animations**: Adjust timing and easing in CSS files
- **Layout**: Modify component structure and styling
- **API**: Update endpoint URLs in component files

## 🧪 Testing

### **Available Scripts**
```bash
npm test          # Run test suite
npm run build     # Build for production
npm run eject     # Eject from Create React App
```

## 🚀 Deployment

### **Build Process**
1. Run `npm run build`
2. Deploy the `build` folder to your hosting service
3. Ensure the backend API is accessible from the frontend domain

### **Environment Setup**
- Set up proxy configuration for production
- Configure CORS on backend for production domain
- Set up environment variables for API endpoints

## 📄 License

This project is part of the Conversational AI Backend Service demonstration.

---

**Repository**: https://github.com/varuntd1234/Think41ass 