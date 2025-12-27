import React, { useState } from 'react';

function App() {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSendMessage = async () => {
    if (!inputText.trim()) return;

    const userMessage = {
      id: Date.now(),
      text: inputText,
      sender: 'user',
      timestamp: new Date().toLocaleTimeString()
    };

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
          query: inputText,
          generate_chart: true,
          chart_type: 'auto'
        }),
      });

      const data = await response.json();
      
      const assistantMessage = {
        id: Date.now() + 1,
        text: data.response || 'No response received',
        sender: 'assistant',
        timestamp: new Date().toLocaleTimeString(),
        chart_path: data.chart_path
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        text: `Error: ${error.message}`,
        sender: 'assistant',
        timestamp: new Date().toLocaleTimeString()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>MongoDB Analytics Agent</h1>
      
      <div style={{ 
        border: '1px solid #ccc', 
        height: '400px', 
        overflow: 'auto', 
        padding: '10px', 
        marginBottom: '10px',
        backgroundColor: '#f9f9f9'
      }}>
        {messages.map(msg => (
          <div key={msg.id} style={{ 
            marginBottom: '10px', 
            textAlign: msg.sender === 'user' ? 'right' : 'left' 
          }}>
            <div style={{
              display: 'inline-block',
              padding: '8px 12px',
              borderRadius: '8px',
              backgroundColor: msg.sender === 'user' ? '#007bff' : '#e9ecef',
              color: msg.sender === 'user' ? 'white' : 'black',
              maxWidth: '70%'
            }}>
              <div>{msg.text}</div>
              {msg.chart_path && (
                <img 
                  src={`http://localhost:8001${msg.chart_path}`} 
                  alt="Chart" 
                  style={{ width: '100%', marginTop: '8px' }}
                />
              )}
              <small style={{ opacity: 0.7 }}>{msg.timestamp}</small>
            </div>
          </div>
        ))}
        {isLoading && (
          <div style={{ textAlign: 'center', color: '#666' }}>
            Analyzing data...
          </div>
        )}
      </div>

      <div style={{ display: 'flex', gap: '10px' }}>
        <input
          type="text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
          placeholder="Ask about your MongoDB data..."
          style={{ 
            flex: 1, 
            padding: '10px', 
            border: '1px solid #ccc', 
            borderRadius: '4px' 
          }}
        />
        <button 
          onClick={handleSendMessage}
          disabled={isLoading || !inputText.trim()}
          style={{
            padding: '10px 20px',
            backgroundColor: '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          Send
        </button>
      </div>
    </div>
  );
}

export default App;