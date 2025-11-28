import React, { useEffect, useState } from 'react';

const SelectedTextHelper = ({ onSelection }) => {
  const [selectedText, setSelectedText] = useState('');
  const [showPrompt, setShowPrompt] = useState(false);
  const [position, setPosition] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const handleSelectionChange = () => {
      const selection = window.getSelection();
      const text = selection.toString().trim();

      if (text && text.length > 0) {
        setSelectedText(text);
        
        // Get the bounding rectangle of the selection
        const range = selection.getRangeAt(0);
        const rect = range.getBoundingClientRect();
        
        // Position the prompt near the selected text
        setPosition({
          x: rect.right + window.scrollX + 5, // A bit to the right of the selection
          y: rect.top + window.scrollY + 5   // A bit below the selection
        });
        setShowPrompt(true);
      } else {
        setSelectedText('');
        setShowPrompt(false);
      }
    };

    document.addEventListener('mouseup', handleSelectionChange);
    document.addEventListener('keyup', handleSelectionChange); // For keyboard selections

    return () => {
      document.removeEventListener('mouseup', handleSelectionChange);
      document.removeEventListener('keyup', handleSelectionChange);
    };
  }, []);

  const handlePromptClick = () => {
    if (onSelection && selectedText) {
      onSelection(selectedText);
    }
    setShowPrompt(false); // Hide prompt after acting
  };

  if (!showPrompt) {
    return null;
  }

  return (
    <div
      style={{
        position: 'absolute',
        top: `${position.y}px`,
        left: `${position.x}px`,
        backgroundColor: '#f0f0f0',
        border: '1px solid #ccc',
        padding: '5px 10px',
        borderRadius: '5px',
        cursor: 'pointer',
        zIndex: 9999, // Ensure it's above other content
        boxShadow: '0 2px 5px rgba(0,0,0,0.2)',
      }}
      onClick={handlePromptClick}
    >
      Ask about "{selectedText.substring(0, 20)}..."
    </div>
  );
};

export default SelectedTextHelper;