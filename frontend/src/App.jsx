import React, { useState } from 'react';
import axios from 'axios';
import ChatBox from './components/ChatBox';

function App() {
  return (
    <div className="bg-gray-100 min-h-screen flex flex-col justify-center items-center">
      <h1 className="text-4xl font-bold mb-6">AI-Powered Chatbot</h1>
      <ChatBox />
    </div>
  );
}

export default App;
