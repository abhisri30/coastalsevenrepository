import React, { useState, useEffect } from 'react';
import img from '../../assets/blackLandingimage.jpg';
import '../../Styles/Landing.css';
import NavBar from '../../Components/NavBar';

const Landing = () => {
  const [showTyping, setShowTyping] = useState(false);

  return (
    <div className="landing-page">
      <NavBar />
      <div
        className="landing-container"
        onMouseEnter={() => setShowTyping(true)}
        onMouseLeave={() => setShowTyping(false)}
      >
        <img src={img} alt="Landing" className="landing-image" />
        {showTyping && <TypingOverlay />}
      </div>
    </div>
  );
};

const TypingOverlay = () => {
  const lines = [
    { text: 'Welcome to', className: 'line-welcome' },
    { text: 'Coastal Seven Consulting', className: 'line-name' },
    { text: 'Are you ready to explore?', className: 'line-ready' },
  ];

  const [typedLines, setTypedLines] = useState(lines.map(() => ''));
  const [currentLineIndex, setCurrentLineIndex] = useState(0);
  const [currentCharIndex, setCurrentCharIndex] = useState(0);

  useEffect(() => {
    let timeoutId;
    if (currentLineIndex < lines.length) {
      if (currentCharIndex < lines[currentLineIndex].text.length) {
        timeoutId = setTimeout(() => {
          setTypedLines(prev => {
            const newLines = [...prev];
            newLines[currentLineIndex] += lines[currentLineIndex].text[currentCharIndex];
            return newLines;
          });
          setCurrentCharIndex(prev => prev + 1);
        }, 50);
      } else {
        timeoutId = setTimeout(() => {
          setCurrentLineIndex(prev => prev + 1);
          setCurrentCharIndex(0);
        }, 300);
      }
    }
    return () => clearTimeout(timeoutId);
  }, [currentCharIndex, currentLineIndex, lines]);

  return (
    <div className="typing-overlay">
      {typedLines.map((line, idx) => (
        <div key={idx} className={`typed-line ${lines[idx].className}`}>
          {line}
        </div>
      ))}
    </div>
  );
};

export default Landing;