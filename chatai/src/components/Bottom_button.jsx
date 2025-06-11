import React from 'react';
// Removed Chat.css import if Bottom_button has its own specific CSS
// and doesn't rely on general sidebar classes from Chat.css for its internal structure.
// If it DOES rely on .sidebar.collapsed for example, keep it or move relevant parts.
// For this example, we assume Bottom_button.css handles all its states.
// import "../styles/Chat.css"; // Potentially remove if not needed for context
import "./Bottom_button.css"; // Component-specific styles

const Bottom_button = ({ icon: Icon, label, onClick, showLabel }) => {
  return (
    <button className="bottom-button" onClick={onClick} aria-label={label}>
      <Icon className="icon" aria-hidden="true" />
      {/* Conditionally render the span itself, not just control visibility with CSS,
          though CSS will also hide it on small screens regardless of showLabel */}
      {showLabel && <span className="label">{label}</span>}
    </button>
  );
};

export default Bottom_button;