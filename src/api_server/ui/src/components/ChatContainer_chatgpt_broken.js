import React, { useState } from 'react';
import MessageBubble from './MessageBubble';

const ChatContainer = ({ messages, onSendMessage, loading, messagesEndRef }) => {
  const [inputValue, setInputValue] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (inputValue.trim()) {
      onSendMessage(inputValue);
      setInputValue('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const examplePrompts = [
    {
      title: "Revenue Analytics",
      prompt: "What was the total revenue last month?"
    },
    {
      title: "Customer Insights", 
      prompt: "Who are the top 5 customers by spending?"
    },
    {
      title: "Menu Performance",
      prompt: "Which menu items are most popular?"
    },
    {
      title: "Order Analysis",
      prompt: "Show me order trends by day of week"
    }
  ];

  return (
    <div className="chat-container">
      {messages.length === 0 ? (
        <div className="empty-state">
          <h1>MongoDB Analytics Agent</h1>
          <p>Ask questions about your restaurant data and get insights with charts</p>
          
          <div className="example-prompts">
            {examplePrompts.map((example, index) => (
              <div 
                key={index}
                className="example-prompt"
                onClick={() => onSendMessage(example.prompt)}
              >
                <h3>{example.title}</h3>
                <p>{example.prompt}</p>
              </div>
            ))}
          </div>
        </div>
      ) : (
        <div className="messages-container">
          {messages.map((message) => (
            <MessageBubble key={message.id} message={message} />
          ))}
          
          {loading && (
            <div className="message assistant">
              <div className="message-content">
                <div className="loading">
                  <div className="loading-dots">
                    <div className="loading-dot"></div>
                    <div className="loading-dot"></div>
                    <div className="loading-dot"></div>
                  </div>
                  <span>Analyzing data...</span>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>
      )}

      <div className="input-container">
        <form onSubmit={handleSubmit} className="input-wrapper">
          <textarea
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Message MongoDB Analytics Agent"
            className="message-input"
            rows={1}
          />
          <button 
            type="submit" 
            disabled={!inputValue.trim() || loading}
            className="send-button"
          >
            <svg className="send-icon" viewBox="0 0 24 24" fill="none">
              <path d="M7 11L12 6L17 11M12 18V7" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </button>
        </form>
      </div>
    </div>
  );
};

export default ChatContainer;