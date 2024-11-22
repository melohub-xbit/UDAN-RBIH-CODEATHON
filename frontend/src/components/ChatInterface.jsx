import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MessageSquare, Send, Sparkles } from 'lucide-react';
import styled from 'styled-components';
// Add this at the top with other imports
const DocumentOption = styled(motion.div)`
  padding: 0.8rem 1.2rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  cursor: pointer;
  border: 1px solid rgba(37, 99, 235, 0.2);
  transition: all 0.2s ease;
  position: relative;
  
  &:hover {
    background: rgba(37, 99, 235, 0.1);
    transform: translateY(-2px);
  }
  
  &.selected {
    background: rgba(37, 99, 235, 0.2);
    border-color: #2563eb;
  }
`;

const Tooltip = styled(motion.div)`
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-size: 0.9rem;
  pointer-events: none;
  white-space: nowrap;
  z-index: 10;
`;

const OptionsContainer = styled(motion.div)`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  margin: 1rem 0;
`;


const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);
  const documentOptions = [
    { id: 1, name: "Aadhaar Card", purpose: "Primary ID proof required for all loans" },
    { id: 2, name: "PAN Card", purpose: "Mandatory for tax verification" },
    { id: 3, name: "Bank Statements", purpose: "Shows financial transaction history" },
    { id: 4, name: "Business License", purpose: "Proves business legitimacy" },
    { id: 5, name: "Income Tax Returns", purpose: "Validates income claims" },
    { id: 6, name: "Property Documents", purpose: "Required for secured loans" },
    { id: 7, name: "Utility Bills", purpose: "Address proof verification" },
    { id: 8, name: "GST Returns", purpose: "Business transaction proof" }
  ];
  const [selectedDocs, setSelectedDocs] = useState(new Set());
const [hoveredDoc, setHoveredDoc] = useState(null);
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    setIsTyping(true);
    setTimeout(() => {
      setMessages([
        {
          text: "✨ Welcome! How can I assist you today?",
          isBot: true
        }
      ]);
      setIsTyping(false);
    }, 1500);
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const handleSend = () => {
    if (input.trim()) {
      setMessages([...messages, { text: input, isBot: false }]);
      setInput('');
      setIsTyping(true);
      
      setTimeout(() => {
        setIsTyping(false);
        setMessages(prev => [...prev, {
          text: "Processing your request... ✨",
          isBot: true
        }]);
      }, 2000);
    }
  };

  return (
    <div className="relative min-h-screen w-full bg-blue-600 p-4 overflow-hidden">
      {/* Animated Background Patterns */}
      <motion.div
        className="absolute top-0 left-0 w-full h-full"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
      >
        {/* Abstract Wave Pattern */}
        <svg className="absolute w-full h-full opacity-20" viewBox="0 0 100 100" preserveAspectRatio="none">
          <motion.path
            d="M0,50 Q25,30 50,50 T100,50 V100 H0 Z"
            fill="rgba(255,255,255,0.1)"
            animate={{
              d: [
                "M0,50 Q25,30 50,50 T100,50 V100 H0 Z",
                "M0,50 Q25,70 50,50 T100,50 V100 H0 Z",
                "M0,50 Q25,30 50,50 T100,50 V100 H0 Z"
              ]
            }}
            transition={{
              duration: 10,
              repeat: Infinity,
              ease: "linear"
            }}
          />
        </svg>
      </motion.div>

      {/* Floating Elements */}
      <motion.div
        className="absolute top-20 left-20 w-32 h-32 bg-yellow-300 rounded-full blur-3xl"
        animate={{
          scale: [1, 1.2, 1],
          opacity: [0.2, 0.3, 0.2],
          x: [-10, 10, -10],
          y: [-10, 10, -10],
        }}
        transition={{
          duration: 8,
          repeat: Infinity,
        }}
      />
      <motion.div
        className="absolute bottom-40 right-20 w-40 h-40 bg-blue-400 rounded-full blur-3xl"
        animate={{
          scale: [1.2, 1, 1.2],
          opacity: [0.1, 0.2, 0.1],
          x: [10, -10, 10],
          y: [10, -10, 10],
        }}
        transition={{
          duration: 10,
          repeat: Infinity,
        }}
      />

      {/* Main Chat Container */}
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="container mx-auto h-screen max-w-6xl rounded-3xl overflow-hidden backdrop-blur-xl bg-gradient-to-br from-blue-600/40 via-blue-500/30 to-blue-400/40 border border-white/20 shadow-2xl"
      >
        {/* Header */}
        <div className="bg-gradient-to-r from-blue-500 to-blue-600 p-6 flex items-center justify-between border-b border-white/20">
          <motion.div 
            className="flex items-center gap-4"
            initial={{ x: -20 }}
            animate={{ x: 0 }}
          >
            <motion.div
              animate={{
                scale: [1, 1.2, 1],
                rotate: [0, 360],
              }}
              transition={{
                duration: 3,
                repeat: Infinity,
              }}
            >
              <Sparkles className="w-8 h-8 text-yellow-300" />
            </motion.div>
            <h1 className="text-2xl font-bold text-white">Chat Assistant</h1>
          </motion.div>
          <motion.div
            className="flex items-center gap-2 bg-blue-700/40 px-4 py-2 rounded-full"
            animate={{
              backgroundColor: ["rgba(29, 78, 216, 0.4)", "rgba(37, 99, 235, 0.4)", "rgba(29, 78, 216, 0.4)"],
            }}
            transition={{ duration: 2, repeat: Infinity }}
          >
            <div className="w-2 h-2 bg-green-400 rounded-full" />
            <span className="text-white text-sm">Online</span>
          </motion.div>
        </div>

        {/* Messages Area */}
        <div className="h-[calc(100vh-12rem)] overflow-y-auto p-6 space-y-4">
          <AnimatePresence>
            {messages.map((message, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20, scale: 0.95 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                exit={{ opacity: 0, scale: 0.95 }}
                className={`flex ${message.isBot ? 'justify-start' : 'justify-end'}`}
              >
                <div
                  className={`max-w-[70%] p-4 rounded-2xl shadow-lg ${
                    message.isBot
                      ? 'bg-white/20 text-white backdrop-blur-sm border border-white/10'
                      : 'bg-gradient-to-r from-yellow-400 to-yellow-500 text-white'
                  }`}
                >
                  {message.text}
                </div>
              </motion.div>
            ))}
            
            {isTyping && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="flex gap-2 p-4 w-20 bg-white/20 rounded-xl"
              >
                {[0, 1, 2].map((i) => (
                  <motion.div
                    key={i}
                    className="w-2 h-2 bg-white rounded-full"
                    animate={{ y: [0, -6, 0] }}
                    transition={{
                      duration: 0.6,
                      repeat: Infinity,
                      delay: i * 0.2,
                    }}
                  />
                ))}
              </motion.div>
            )}
          </AnimatePresence><OptionsContainer
    initial={{ opacity: 0 }}
    animate={{ opacity: 1 }}
    transition={{ duration: 0.5 }}
  >
    {documentOptions.map((doc) => (
      <DocumentOption
        key={doc.id}
        className={selectedDocs.has(doc.id) ? 'selected' : ''}
        onClick={() => {
          const newSelected = new Set(selectedDocs);
          if (newSelected.has(doc.id)) {
            newSelected.delete(doc.id);
          } else {
            newSelected.add(doc.id);
          }
          setSelectedDocs(newSelected);
        }}
        onMouseEnter={() => setHoveredDoc(doc)}
        onMouseLeave={() => setHoveredDoc(null)}
      >
        {doc.name}
        {hoveredDoc?.id === doc.id && (
          <Tooltip
            initial={{ opacity: 0, y: 5 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
          >
            {doc.purpose}
          </Tooltip>
        )}
      </DocumentOption>
    ))}
  </OptionsContainer>

  <div ref={messagesEndRef} />
</div>
       
        {/* Input Area */}
        <div className="absolute bottom-0 w-full p-6 bg-blue-600/50 backdrop-blur-md border-t border-white/20">
          <div className="flex gap-4">
            <motion.input
              whileFocus={{ scale: 1.01 }}
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSend()}
              className="flex-1 bg-white/20 text-white placeholder-white/60 rounded-xl px-6 py-4 focus:outline-none focus:ring-2 focus:ring-yellow-400/50"
              placeholder="Type your message..."
            />
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={handleSend}
              className="bg-gradient-to-r from-yellow-400 to-yellow-500 text-white px-6 py-4 rounded-xl flex items-center gap-2 font-semibold shadow-lg"
            >
              <Send className="w-5 h-5" />
              Send
            </motion.button>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default ChatInterface;
