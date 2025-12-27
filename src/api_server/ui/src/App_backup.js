import React, { useState, useRef, useEffect } from 'react';
import ChatContainer from './components/ChatContainer';
import MetricTile from './components/MetricTile';
import './index.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [tools, setTools] = useState([]);
  const [showSidebar, setShowSidebar] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Fetch available tools
  useEffect(() => {
    fetchTools();
  }, []);

  const fetchTools = async () => {
    try {
      const response = await fetch('http://localhost:8001/tools');
      if (response.ok) {
        const data = await response.json();
        setTools(data.tools || []);
      }
    } catch (error) {
      console.error('Failed to fetch tools:', error);
    }
  };

  const sendMessage = async (text) => {
    if (!text.trim()) return;

    const userMessage = { role: 'user', content: text };
    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8001/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: text,
          generate_chart: false
        }),
      });

      if (response.ok) {
        const data = await response.json();
        if (data.success) {
          let messageContent = data.response;
          
          const assistantMessage = { 
            role: 'assistant', 
            content: messageContent,
            chart_path: data.chart_path,
            chart_title: data.chart_title
          };
          setMessages(prev => [...prev, assistantMessage]);
        } else {
          const errorMessage = { 
            role: 'assistant', 
            content: data.error || 'An error occurred while processing your request.' 
          };
          setMessages(prev => [...prev, errorMessage]);
        }
      } else {
        throw new Error(`Server responded with status: ${response.status}`);
      }
    } catch (error) {
      console.error('Error:', error);
      const errorMessage = { 
        role: 'assistant', 
        content: 'Sorry, I encountered an error while processing your request. Please make sure the backend server is running on port 8001.' 
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    sendMessage(inputText);
  };

  const handleExampleClick = (exampleText) => {
    sendMessage(exampleText);
  };

  const startNewChat = () => {
    setMessages([]);
  };

  return (
    <div className="h-screen bg-slate-50 flex">
      {/* Sidebar - Minimal Control Panel */}
      <div className={`${showSidebar ? 'w-80' : 'w-16'} transition-all duration-300 bg-white border-r border-slate-200 flex flex-col`}>
        {/* Header */}
        <div className="p-4 border-b border-slate-200">
          <div className="flex items-center justify-between">
            <button
              onClick={() => setShowSidebar(!showSidebar)}
              className="w-8 h-8 flex items-center justify-center rounded-lg hover:bg-slate-100 transition-colors"
            >
              <span className="text-slate-600">☰</span>
            </button>
            {showSidebar && (
              <h1 className="text-lg font-semibold text-slate-900">X-Hotel Analytics</h1>
            )}
          </div>
        </div>

        {/* Tools and Controls */}
        <div className="flex-1 p-4">
          {showSidebar && (
            <>
              <div className="mb-6">
                <button
                  onClick={startNewChat}
                  className="w-full px-4 py-2 bg-brand-600 text-white rounded-lg hover:bg-brand-700 transition-colors font-medium"
                >
                  New Analysis
                </button>
              </div>

              {/* MCP Tools Count */}
              <div className="mb-6">
                <div className="bg-slate-50 rounded-lg p-3">
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-slate-600">MCP Tools</span>
                    <span className="font-medium text-slate-900">{tools.length}</span>
                  </div>
                </div>
              </div>

              {/* Quick Metrics */}
              <div className="space-y-3">
                <h3 className="text-sm font-medium text-slate-700 mb-3">Quick Stats</h3>
                <MetricTile 
                  label="Active Session"
                  value={messages.length > 0 ? "Running" : "Ready"}
                  icon="🔄"
                />
                <MetricTile 
                  label="Messages"
                  value={messages.length}
                  icon="💬"
                />
              </div>
            </>
          )}
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Top Bar */}
        <div className="bg-white border-b border-slate-200 px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-xl font-semibold text-slate-900">MongoDB Analytics Assistant</h2>
              <p className="text-sm text-slate-600">Powered by MCP • Ask questions about your hotel data</p>
            </div>
            <div className="flex items-center space-x-3">
              <div className="flex items-center space-x-2 text-sm text-slate-600">
                <div className="w-2 h-2 bg-emerald-500 rounded-full"></div>
                <span>Connected</span>
              </div>
            </div>
          </div>
        </div>

        {/* Chat Container */}
        <ChatContainer 
          messages={messages}
          isLoading={isLoading}
          messagesEndRef={messagesEndRef}
          onExampleClick={handleExampleClick}
        />

        {/* Input Area */}
        <div className="bg-white border-t border-slate-200 p-6">
          <div className="max-w-4xl mx-auto">
            <form onSubmit={handleSubmit} className="relative">
              <div className="flex items-end space-x-3">
                <div className="flex-1">
                  <textarea
                    value={inputText}
                    onChange={(e) => setInputText(e.target.value)}
                    onKeyDown={(e) => {
                      if (e.key === 'Enter' && !e.shiftKey) {
                        e.preventDefault();
                        handleSubmit(e);
                      }
                    }}
                    placeholder="Ask about your hotel analytics... (e.g., 'Show me today's revenue breakdown')"
                    className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-brand-500 focus:border-brand-500 resize-none transition-colors"
                    rows={1}
                    style={{
                      minHeight: '44px',
                      maxHeight: '120px',
                      resize: 'none'
                    }}
                    disabled={isLoading}
                  />
                </div>
                <button
                  type="submit"
                  disabled={isLoading || !inputText.trim()}
                  className="px-6 py-3 bg-brand-600 text-white rounded-lg hover:bg-brand-700 disabled:bg-slate-300 disabled:cursor-not-allowed transition-colors font-medium"
                >
                  {isLoading ? (
                    <div className="flex items-center space-x-2">
                      <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                      <span>Analyzing...</span>
                    </div>
                  ) : (
                    'Send'
                  )}
                </button>
              </div>
            </form>
            
            <div className="mt-3 flex items-center justify-center space-x-4 text-xs text-slate-500">
              <span>Shift + Enter for new line</span>
              <span>•</span>
              <span>Connected to MongoDB via MCP</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;