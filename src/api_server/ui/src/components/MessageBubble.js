import React from 'react';

const MessageBubble = ({ message, isUser }) => {
  const formatMessage = (content) => {
    if (!content) return null;
    
    // Split by double newlines for paragraphs
    const paragraphs = content.split('\\n\\n');
    
    return paragraphs.map((paragraph, pIndex) => {
      // Split by single newlines within paragraphs
      const lines = paragraph.split('\\n');
      
      return (
        <div key={pIndex} className="mb-3 last:mb-0">
          {lines.map((line, lIndex) => {
            if (line.trim() === '') return null;
            
            // Handle headers (lines starting with ###, ##, #)
            if (line.match(/^#{1,3}\\s/)) {
              const level = line.match(/^(#{1,3})/)[1].length;
              const text = line.replace(/^#{1,3}\\s/, '');
              const headerClass = level === 1 ? 'text-xl font-bold text-slate-900 mb-2' :
                                 level === 2 ? 'text-lg font-semibold text-slate-800 mb-2' :
                                 'text-base font-medium text-slate-700 mb-1';
              return (
                <div key={lIndex} className={headerClass}>
                  {text}
                </div>
              );
            }
            
            // Handle bullet points
            if (line.match(/^[•\\-\\*]\\s/)) {
              const text = line.replace(/^[•\\-\\*]\\s/, '');
              return (
                <div key={lIndex} className="flex items-start mb-1">
                  <span className="text-brand-600 mr-2 font-medium">•</span>
                  <span className="flex-1">{formatInlineText(text)}</span>
                </div>
              );
            }
            
            // Handle numbered lists
            if (line.match(/^\\d+\\.\\s/)) {
              return (
                <div key={lIndex} className="mb-1 font-medium">
                  {formatInlineText(line)}
                </div>
              );
            }
            
            // Handle code blocks or data
            if (line.match(/^\\s{2,}/) || (line.includes(':') && line.includes('$')) || line.match(/^\\w+_\\w+:/)) {
              return (
                <div key={lIndex} className="bg-slate-50 border border-slate-200 rounded px-3 py-2 mb-2 font-mono text-sm text-slate-700">
                  {line}
                </div>
              );
            }
            
            // Handle chart image rendering
            const imgMatch = line.match(/!\\[(.*?)\\]\\((.*?)\\)/);
            if (imgMatch) {
              const [, altText, imageUrl] = imgMatch;
              return (
                <div key={lIndex} className="my-4">
                  <img 
                    src={imageUrl} 
                    alt={altText}
                    className="w-full max-w-lg rounded-lg border border-slate-200 shadow-sm"
                  />
                </div>
              );
            }
            
            // Regular text lines
            return (
              <div key={lIndex} className="mb-2 last:mb-0 leading-relaxed">
                {formatInlineText(line)}
              </div>
            );
          })}
        </div>
      );
    });
  };
  
  const formatInlineText = (text) => {
    // Handle bold text (**text**)
    text = text.replace(/\\*\\*(.*?)\\*\\*/g, '<strong class="font-semibold text-slate-900">$1</strong>');
    // Handle code (`text`)
    text = text.replace(/`(.*?)`/g, '<code class="bg-slate-100 px-1 py-0.5 rounded text-sm font-mono text-slate-700">$1</code>');
    // Handle numbers and currency
    text = text.replace(/(\\$[\\d,]+\\.?\\d*)/g, '<span class="font-semibold text-emerald-600">$1</span>');
    text = text.replace(/\\b(\\d+)\\b/g, '<span class="font-medium text-brand-600">$1</span>');
    
    return <span dangerouslySetInnerHTML={{ __html: text }} />;
  };

  if (isUser) {
    return (
      <div className="flex justify-end mb-6">
        <div className="flex items-start space-x-3 max-w-3xl">
          <div className="bg-brand-600 text-white rounded-lg px-4 py-3 max-w-full">
            <p className="text-sm leading-relaxed">{message.content}</p>
          </div>
          <div className="w-8 h-8 bg-brand-100 rounded-full flex items-center justify-center flex-shrink-0">
            <span className="text-brand-600 text-sm">👤</span>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex justify-start mb-6">
      <div className="flex items-start space-x-3 max-w-4xl">
        <div className="w-8 h-8 bg-slate-100 rounded-full flex items-center justify-center flex-shrink-0">
          <span className="text-slate-600 text-sm">🤖</span>
        </div>
        <div className="bg-white border border-slate-200 rounded-lg px-4 py-3 shadow-sm flex-1">
          <div className="text-sm text-slate-700 leading-relaxed">
            {formatMessage(message.content)}
          </div>
          
          {/* Display chart if available */}
          {message.chart_path && (
            <div className="mt-4 pt-4 border-t border-slate-100">
              <img 
                src={`http://localhost:8001${message.chart_path}`}
                alt={message.chart_title || "Generated Chart"}
                className="w-full max-w-2xl rounded-lg border border-slate-200 shadow-sm"
                onError={(e) => {
                  console.error('Failed to load chart:', message.chart_path);
                  e.target.style.display = 'none';
                }}
              />
              {message.chart_title && (
                <p className="text-sm text-slate-600 mt-2 font-medium">
                  📊 {message.chart_title}
                </p>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default MessageBubble;