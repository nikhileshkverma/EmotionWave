import { useState, useEffect, useRef } from "react";
import { FaTimes, FaMicrophone, FaRegThumbsUp, FaRegThumbsDown, FaVolumeUp } from "react-icons/fa";
import { IoMdSend } from "react-icons/io";

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

export default function ChatApp() {
  const [messages, setMessages] = useState([
    { sender: "bot", text: "Hello! I'm EmotionWave. How are you feeling today?" }
  ]);
  const [input, setInput] = useState("");
  const [isOpen, setIsOpen] = useState(false);
  const [hasNewMessage, setHasNewMessage] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;
    const userText = input.trim();

    setMessages(prev => [...prev, { sender: "user", text: userText }]);
    setInput("");
    setMessages(prev => [...prev, { sender: "bot", text: "Thinking..." }]);

    // Prepare correct conversation history
    const conversationHistory = messages
      .filter(m => m.sender === "user" || m.sender === "bot")
      .map(m => ({
        role: m.sender === "bot" ? "assistant" : "user",
        content: m.text
      }));

    conversationHistory.push({ role: "user", content: userText });

    try {
      const res = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ history: conversationHistory }),
      });

      const { reply } = await res.json();
      setMessages(prev =>
        prev.map((msg, idx) =>
          idx === prev.length - 1
            ? { sender: "bot", text: reply }
            : msg
        )
      );
      if (!isOpen) {
        setHasNewMessage(true);
      }
    } catch {
      setMessages(prev =>
        prev.map((msg, idx) =>
          idx === prev.length - 1
            ? { sender: "bot", text: "Oops, something went wrong." }
            : msg
        )
      );
    }
  };

  const getTimeNow = () => {
    return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const startListening = () => {
    if (!SpeechRecognition) {
      alert("Speech Recognition not supported in this browser!");
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = 'en-US';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.start();

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      setInput(transcript);
    };

    recognition.onerror = (event) => {
      console.error('Speech recognition error:', event.error);
    };
  };

  const speakText = (text) => {
    if (!window.speechSynthesis) {
      console.error("Speech Synthesis not supported in this browser.");
      return;
    }

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'en-US';
    window.speechSynthesis.speak(utterance);
  };

  return (
    <div
      className="relative min-h-screen bg-cover bg-center"
      style={{
        backgroundImage: "url('/images/what-are-chatbots.jpg')"
      }}
    >
      {!isOpen && (
        <div className="fixed bottom-4 right-4 flex flex-col items-center space-y-2">
          <div className="bg-gray-800 text-white text-xs px-3 py-1 rounded-full shadow-md animate-bounce">
            Click me to chat!
          </div>
          <button
            onClick={() => {
              setIsOpen(true);
              setHasNewMessage(false);
            }}
            className="bg-blue-600 text-white p-4 rounded-full shadow-lg hover:bg-blue-700"
          >
            💬
            {hasNewMessage && (
              <span className="absolute top-0 right-0 w-3 h-3 bg-red-500 rounded-full border-2 border-white"></span>
            )}
          </button>
        </div>
      )}

      {isOpen && (
        <div className="fixed bottom-20 right-4 w-80 h-[500px] bg-white/80 backdrop-blur-md border shadow-xl rounded-3xl flex flex-col transform transition-all duration-300 ease-in-out">
          <div className="flex items-center justify-between bg-gradient-to-r from-blue-600 to-indigo-600 text-white p-4 rounded-t-3xl">
            <div className="flex items-center gap-2">
              <div className="bg-white p-1 rounded-full">
                <span role="img" aria-label="robot">🤖</span>
              </div>
              <h1 className="text-md font-semibold">EmotionWave</h1>
            </div>
            <button onClick={() => setIsOpen(false)} className="hover:text-gray-300">
              <FaTimes size={18} />
            </button>
          </div>

          <div className="flex-1 p-4 overflow-y-auto space-y-3">
            {messages.map((msg, idx) => (
              <div key={idx} className={`flex ${msg.sender === "user" ? "justify-end" : "justify-start"}`}>
                <div className={`max-w-[75%] p-3 rounded-2xl shadow ${msg.sender === "user" ? "bg-blue-500 text-white" : "bg-white text-gray-800"}`}>
                  <p className="text-sm leading-relaxed">{msg.text}</p>
                  <div className="text-[10px] flex items-center gap-1 mt-1">
                    {msg.sender === "bot" && (
                      <>
                        <button><FaRegThumbsUp size={10} /></button>
                        <button><FaRegThumbsDown size={10} /></button>
                        <button onClick={() => speakText(msg.text)}><FaVolumeUp size={10} /></button>
                      </>
                    )}
                    <span>{getTimeNow()}</span>
                  </div>
                </div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>

          <div className="flex items-center gap-2 p-3 border-t bg-white/70 backdrop-blur-md rounded-b-3xl">
            <input
              type="text"
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={e => e.key === "Enter" && handleSend()}
              placeholder="Type a message..."
              className="flex-1 border border-gray-300 rounded-full px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
            />
            <button onClick={handleSend} className="p-2 bg-blue-500 rounded-full text-white hover:bg-blue-600">
              <IoMdSend size={18} />
            </button>
            <button onClick={startListening} className="p-2 bg-gray-200 rounded-full hover:bg-gray-300">
              <FaMicrophone size={18} />
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
