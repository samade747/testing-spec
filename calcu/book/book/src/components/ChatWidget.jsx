import React, { useState } from 'react';
import styles from './ChatWidget.module.css'; // Assuming CSS module for styling

const ChatWidget = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const toggleChat = () => {
    setIsOpen(!isOpen);
    // Clear state when closing
    if (isOpen) {
      setQuestion('');
      setResponse(null);
      setError(null);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;

    setIsLoading(true);
    setError(null);
    setResponse(null);

    // Placeholder for actual API call
    try {
      const apiResponse = await fetch('/api/query', { // Assuming /api/query is proxied to backend
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question }),
      });

      if (!apiResponse.ok) {
        throw new Error(`HTTP error! status: ${apiResponse.status}`);
      }

      const data = await apiResponse.json();
      setResponse(data);
    } catch (err) {
      setError('Failed to fetch response. Please try again.');
      console.error('ChatWidget API error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={styles.chatContainer}>
      <button className={styles.chatToggle} onClick={toggleChat}>
        {isOpen ? 'Close Chat' : 'Open Chat'}
      </button>

      {isOpen && (
        <div className={styles.chatWindow}>
          <div className={styles.chatHeader}>
            <h3>Ask the Book</h3>
          </div>
          <div className={styles.chatBody}>
            {isLoading && <p>Thinking...</p>}
            {error && <p className={styles.error}>{error}</p>}
            {response && (
              <div className={styles.response}>
                <h4>Answer:</h4>
                <p>{response.answer}</p>
                {response.contexts && response.contexts.length > 0 && (
                  <div className={styles.contexts}>
                    <h5>Contexts:</h5>
                    <ul>
                      {response.contexts.map((ctx, index) => (
                        <li key={index}>
                          <strong>Source:</strong> {ctx.source || 'N/A'} <br />
                          {ctx.text.substring(0, 100)}...
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}
          </div>
          <form onSubmit={handleSubmit} className={styles.chatInputForm}>
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Ask a question..."
              className={styles.chatInput}
              disabled={isLoading}
            />
            <button type="submit" disabled={isLoading} className={styles.chatSendButton}>
              Send
            </button>
          </form>
        </div>
      )}
    </div>
  );
};

export default ChatWidget;
