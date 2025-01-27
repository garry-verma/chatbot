import React, { useState } from 'react';
import axios from 'axios';
import ChatMessage from './ChatMessage';

function ChatBox() {
  const [messages, setMessages] = useState([]);
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false); // Track loading state

  const handleQuerySubmit = async (e) => {
    e.preventDefault();

    if (!query.trim()) return; // Prevent empty queries

    // Add user query to messages
    const userMessage = { sender: 'user', text: query };
    setMessages((prevMessages) => [...prevMessages, userMessage]);

    setLoading(true); // Set loading while processing
    try {
      // Send query to the backend
      const response = await axios.post('http://localhost:5000/query', { query });
      console.log('Response:', response.data);

      // Add bot response to messages
      const botMessage = {
        sender: 'bot',
        text: response.data.raw_results || 'No data found.',
        summary: response.data.summary || 'No summary available.',
      };
      setMessages((prevMessages) => [...prevMessages, botMessage]);
    } catch (error) {
      console.error('Error:', error);

      // Add error message to messages
      const errorMessage = {
        sender: 'bot',
        text: "Sorry, I couldn't process that.",
        summary: 'No summary available due to an error.',
      };
      setMessages((prevMessages) => [...prevMessages, errorMessage]);
    } finally {
      setLoading(false); // Reset loading state
      setQuery(''); // Clear input
    }
  };

  return (
    <div className="w-full max-w-md p-4 bg-white rounded shadow-md">
      <div className="space-y-4 mb-4">
        {messages.map((msg, index) => (
          <ChatMessage key={index} message={msg} />
        ))}
        {loading && <p className="text-gray-500 text-center">Processing...</p>} {/* Show loading state */}
      </div>
      <form onSubmit={handleQuerySubmit} className="flex space-x-4">
        <input
          type="text"
          className="flex-1 p-2 border border-gray-300 rounded"
          placeholder="Ask me something..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          disabled={loading} // Disable input while loading
        />
        <button
          type="submit"
          className="px-4 py-2 bg-blue-500 text-white rounded"
          disabled={loading} // Disable button while loading
        >
          Send
        </button>
      </form>
    </div>
  );
}

export default ChatBox;
