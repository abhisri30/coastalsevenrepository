import React, { useState } from 'react';
import { HiMenu } from "react-icons/hi";
import { FaPlus } from "react-icons/fa6";
import { FiHelpCircle, FiSettings } from "react-icons/fi";
import { MdOutlineAccessTime } from "react-icons/md";
import { FaFile } from "react-icons/fa6";
import { FaMicrophoneAlt } from "react-icons/fa";
import { RiSendPlane2Fill } from "react-icons/ri";
import { MdAccountCircle } from "react-icons/md";
import { FaRegFilePdf } from "react-icons/fa";
import Bottom_button from '../components/Bottom_button.jsx';
import { retrieveDocument, uploadPDF } from '../api/request.js';
import "../styles/Chat.css";

const Chat = () => {
  const [isExtended, setIsExtended] = useState(false);
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleMenuClick = () => setIsExtended(prev => !prev);

  const handleNewChat = () => setMessages([]);

  const handleSend = async () => {
    if (!input.trim()) return;
    setMessages(prev => [...prev, { type: 'user', text: input }]);
    setInput('');
    setLoading(true);

    try {
      const res = await retrieveDocument(input);
      const generatedText = res?.body?.generation?.generated_text || 'No response generated.';
      setMessages(prev => [...prev, { type: 'bot', text: generatedText }]);
    } catch {
      setMessages(prev => [...prev, { type: 'bot', text: 'Failed to get response from server.' }]);
    }
    setLoading(false);
  };

  const handleFileChange = async (event) => {
    const file = event.target.files[0];
    if (file && file.type === 'application/pdf') {
      setLoading(true);
      try {
        const result = await uploadPDF(file);
        const replyText = result.message || 'File uploaded successfully.';
        setMessages(prev => [...prev, {
          type: 'file',
          fileName: file.name,
          text: replyText,
        }]);
      } catch {
        setMessages(prev => [...prev, {
          type: 'file',
          fileName: file.name,
          text: 'File upload failed.',
        }]);
      }
      setLoading(false);
      event.target.value = null;
    } else if (file) {
      setMessages(prev => [...prev, { type: 'bot', text: 'Please upload a PDF file.' }]);
      event.target.value = null;
    }
  };

  const sidebarClass = `sidebar ${isExtended ? 'extended' : 'collapsed'}`;

  return (
    <div className="chat">
      <div className={sidebarClass}>
        <div className="menu" onClick={handleMenuClick} aria-label={isExtended ? "Collapse menu" : "Expand menu"}>
          <HiMenu />
        </div>
        <button className="new-chat" onClick={handleNewChat} aria-label="New Chat">
          <FaPlus />
          {isExtended && <p>New Chat</p>}
        </button>
        <div className="bottom-section">
          <Bottom_button icon={FiHelpCircle} label="Help" showLabel={isExtended} />
          <Bottom_button icon={FiSettings} label="Settings" showLabel={isExtended} />
          <Bottom_button icon={MdOutlineAccessTime} label="Activity" showLabel={isExtended} />
        </div>
      </div>

      <div className="chat-window">
        <div className="chat-upper">
          <div className="Chat-header"><p>ChatAI</p></div>
          <div className="user-profile">
            <button className="user-profile-btn" aria-label="User Account">
              <MdAccountCircle />
            </button>
          </div>
        </div>

        <div className="chat-middle">
          {messages.length === 0 && !loading ? (
            <div className="initial-prompt">
              <p><span>Hey there!</span></p>
              <p>How can I help you today?</p>
            </div>
          ) : (
            messages.map((msg, i) => {
              if (msg.type === 'file') {
                return (
                  <div key={i} className="chat-message file file-success">
                    <div className="file-info-container">
                      <FaRegFilePdf className="file-icon" />
                      <span className="file-name">{msg.fileName}</span>
                    </div>
                    <div className="file-status-container">
                      <span className="file-status-text">{msg.text}</span>
                    </div>
                  </div>
                );
              }
              return (
                <div key={i} className={`chat-message-${msg.type}`}>
                  <span>{msg.text}</span>
                </div>
              );
            })
          )}
          {loading && (
            <div className="chat-message-bot loading-indicator">
              <span className="chatgpt-dot"></span>
              <span className="chatgpt-dot"></span>
              <span className="chatgpt-dot"></span>
            </div>
          )}
        </div>

        <div className="main-bottom">
          <div className="search-box">
            <input
              type="text"
              placeholder="Type your message here..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && !loading && handleSend()}
              disabled={loading}
            />
            <div>
              <input
                type="file"
                id="file-upload"
                accept="application/pdf"
                style={{ display: 'none' }}
                onChange={handleFileChange}
                disabled={loading}
              />
              <button
                className="icon-btn"
                aria-label="Attach PDF"
                onClick={() => document.getElementById('file-upload').click()}
                disabled={loading}
              >
                <FaFile />
              </button>
              <button className="icon-btn" aria-label="Record Audio" disabled={loading}>
                <FaMicrophoneAlt />
              </button>
            </div>
          </div>
          <button
            className="send-btn"
            onClick={handleSend}
            disabled={loading || !input.trim()}
            aria-label="Send"
          >
            <RiSendPlane2Fill />
          </button>
        </div>
      </div>
    </div>
  );
};

export default Chat;