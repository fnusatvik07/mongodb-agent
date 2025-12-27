import React from 'react';

const MessageBubble = ({ message }) => {
  const isUser = message.sender === 'user';

  // Extract analytics data for display
  const extractAnalytics = (content) => {
    if (typeof content !== 'string') return null;

    const metrics = [];
    
    // Revenue
    const revenueMatch = content.match(/Total Revenue.*?\$?([\d,]+\.?\d*)/i);
    if (revenueMatch) {
      metrics.push({
        label: 'Total Revenue',
        value: `$${revenueMatch[1]}`
      });
    }

    // Orders
    const orderMatch = content.match(/(\d+)\s+orders?/i);
    if (orderMatch) {
      metrics.push({
        label: 'Orders',
        value: orderMatch[1]
      });
    }

    // Customers
    const customerMatch = content.match(/(\d+)\s+customers?/i);
    if (customerMatch) {
      metrics.push({
        label: 'Customers',
        value: customerMatch[1]
      });
    }

    return metrics.length > 0 ? metrics : null;
  };

  const analytics = extractAnalytics(message.content);

  return (
    <div className={`message ${isUser ? 'user' : 'assistant'}`}>
      <div className="message-content">
        {/* Analytics Cards */}
        {analytics && analytics.length > 0 && (
          <div className="analytics-grid">
            {analytics.map((metric, index) => (
              <div key={index} className="metric-card">
                <div className="metric-value">{metric.value}</div>
                <div className="metric-label">{metric.label}</div>
              </div>
            ))}
          </div>
        )}

        {/* Message Text */}
        <div>
          {typeof message.content === 'string' ? message.content : JSON.stringify(message.content)}
        </div>

        {/* Chart Display */}
        {message.chart_path && (
          <div className="chart-container">
            <img 
              src={`http://localhost:8001${message.chart_path}`} 
              alt="Generated Chart" 
              className="chart-image"
            />
          </div>
        )}
      </div>
    </div>
  );
};

export default MessageBubble;