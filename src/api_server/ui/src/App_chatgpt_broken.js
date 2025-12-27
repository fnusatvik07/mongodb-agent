import React, { useState, useRef, useEffect } from 'react';
import './App.css';
import ChatContainer from './components/ChatContainer';

function App() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(scrollToBottom, [messages]);

  const sendMessage = async (message) => {
    if (message.trim() === '') return;

    const userMessage = {
      id: Date.now(),
      content: message,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setLoading(true);

    try {
      const response = await fetch('http://localhost:8001/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          query: message,
          generate_chart: true,
          chart_type: 'auto'
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to get response');
      }

      const data = await response.json();
      
      const assistantMessage = {
        id: Date.now() + 1,
        content: data.response || 'No response received',
        sender: 'assistant',
        timestamp: new Date(),
        chart_path: data.chart_path,
        tool_used: data.tools_used ? data.tools_used.join(', ') : null
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        id: Date.now() + 1,
        content: `Error: ${error.message}`,
        sender: 'assistant',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const newChat = () => {
    setMessages([]);
  };

  return (
    <div className="app">
      {/* Sidebar */}
      <div className={`sidebar ${sidebarOpen ? '' : 'collapsed'}`}>
        <div className="sidebar-content">
          <button className="new-chat-btn" onClick={newChat}>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
              <path d="M12 5v14m-7-7h14" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
            </svg>
            New chat
          </button>
          
          <div className="chat-history">
            <div className="history-section">
              <div className="history-item active">
                MongoDB Analytics
              </div>
            </div>
          </div>
        </div>
        
        <div className="sidebar-footer">
          <div className="user-menu">
            <div className="user-avatar">U</div>
            <span>User</span>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="main-content">
        <button 
          className="sidebar-toggle"
          onClick={() => setSidebarOpen(!sidebarOpen)}
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
            <path d="M3 12h18m-9-9l9 9-9 9" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </button>

        <ChatContainer
          messages={messages}
          onSendMessage={sendMessage}
          loading={loading}
          messagesEndRef={messagesEndRef}
        />
      </div>
    </div>
  );
}

export default App;