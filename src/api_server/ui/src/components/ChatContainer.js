import React from 'react';
import MessageBubble from './MessageBubble';

const ChatContainer = ({ messages, isLoading, messagesEndRef, onExampleClick }) => {
  const TypingIndicator = () => (
    <div className="flex justify-start mb-6">
      <div className="flex items-start space-x-3 max-w-4xl">
        <div className="w-8 h-8 bg-slate-100 rounded-full flex items-center justify-center flex-shrink-0">
          <span className="text-slate-600 text-sm">🤖</span>
        </div>
        <div className="bg-white border border-slate-200 rounded-lg px-4 py-3 shadow-sm">
          <div className="flex items-center space-x-1">
            <div className="w-2 h-2 bg-slate-400 rounded-full typing-dot"></div>
            <div className="w-2 h-2 bg-slate-400 rounded-full typing-dot"></div>
            <div className="w-2 h-2 bg-slate-400 rounded-full typing-dot"></div>
            <span className="ml-2 text-sm text-slate-500">Analyzing your data...</span>
          </div>
        </div>
      </div>
    </div>
  );

  if (messages.length === 0) {
    return (
      <div className="flex-1 flex items-center justify-center">
        <div className="text-center max-w-2xl mx-auto px-6">
          <div className="w-16 h-16 bg-brand-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <span className="text-brand-600 text-2xl">📊</span>
          </div>
          <h2 className="text-2xl font-semibold text-slate-900 mb-3">
            Welcome to X-Hotel Analytics
          </h2>
          <p className="text-lg text-slate-600 mb-8">
            Your intelligent MongoDB-powered analytics assistant. Ask questions about your hotel data and get instant insights.
          </p>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-3xl mx-auto">
            <ExampleCard 
              icon="💰"
              title="Revenue Analytics"
              question="Show me today's revenue breakdown"
              onClick={onExampleClick}
            />
            <ExampleCard 
              icon="🍽️"
              title="Menu Performance"
              question="What are the most popular menu items?"
              onClick={onExampleClick}
            />
            <ExampleCard 
              icon="📈"
              title="Data Visualization"
              question="Generate a revenue chart by order type"
              onClick={onExampleClick}
            />
            <ExampleCard 
              icon="👥"
              title="Customer Insights"
              question="Analyze customer segments and spending"
              onClick={onExampleClick}
            />
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-y-auto scrollbar-thin px-6 py-6">
      <div className="max-w-5xl mx-auto">
        {messages.map((message, index) => (
          <MessageBubble 
            key={index} 
            message={message} 
            isUser={message.role === 'user'} 
          />
        ))}
        {isLoading && <TypingIndicator />}
        <div ref={messagesEndRef} />
      </div>
    </div>
  );
};

const ExampleCard = ({ icon, title, question, onClick }) => (
  <button
    onClick={() => onClick(question)}
    className="p-4 bg-white border border-slate-200 rounded-lg hover:border-brand-300 hover:shadow-md transition-all duration-200 text-left group"
  >
    <div className="flex items-center space-x-3 mb-2">
      <span className="text-xl">{icon}</span>
      <h4 className="font-medium text-slate-900 group-hover:text-brand-700">{title}</h4>
    </div>
    <p className="text-sm text-slate-600 leading-relaxed">{question}</p>
  </button>
);

export default ChatContainer;