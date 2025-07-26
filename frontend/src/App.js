import React from 'react';
import './App.css';
import ChatWindow from './components/ChatWindow';
import { ChatProvider } from './context/ChatContext';

function App() {
  return (
    <ChatProvider>
      <div className="App">
        <ChatWindow />
      </div>
    </ChatProvider>
  );
}

export default App; 