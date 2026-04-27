import { useState, useEffect, useRef } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([]);

  const chatEndRef = useRef(null);

  
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chat]);


  const speak = (text) => {
    const speech = new SpeechSynthesisUtterance(text);
    speech.lang = "en-US";
    window.speechSynthesis.speak(speech);
  };

  
  const startListening = () => {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.start();

    recognition.onresult = (event) => {
      const voiceText = event.results[0][0].transcript;
      sendVoiceMessage(voiceText);
    };
  };

  const sendVoiceMessage = async (voiceText) => {
  const formattedMessages = [
    ...chat.map((c) => ({
      role: c.role === "user" ? "user" : "assistant",
      content: c.text,
    })),
    { role: "user", content: voiceText },
  ];

  setChat((prev) => [...prev, { role: "user", text: voiceText }]);

  try {
    const res = await axios.post(
      "https://your-backend.onrender.com/api/chat/",
      { messages: formattedMessages }
    );

    const reply = res.data.reply;

    setChat((prev) => [...prev, { role: "bot", text: reply }]);

  } catch {
    setChat((prev) => [
      ...prev,
      { role: "bot", text: "Error" },
    ]);
  }
};

 const sendMessage = async () => {
  if (!message.trim()) return;

  const userMsg = message;

  
  const formattedMessages = [
    ...chat.map((c) => ({
      role: c.role === "user" ? "user" : "assistant",
      content: c.text,
    })),
    { role: "user", content: userMsg },
  ];

  setChat((prev) => [...prev, { role: "user", text: userMsg }]);
  setMessage("");

  try {
    const res = await axios.post(
      "https://your-backend.onrender.com/api/chat/",
      { messages: formattedMessages }
    );

    const reply = res.data.reply;

    setChat((prev) => [...prev, { role: "bot", text: reply }]);

  } catch {
    setChat((prev) => [
      ...prev,
      { role: "bot", text: "Error connecting backend" },
    ]);
  }
};
  return (
    <div className="container">
      <h1>🤖 AI Chatbot 🤖</h1>

      <div className="chat-box">
        {chat.map((c, i) => (
          <div key={i} className={c.role === "user" ? "user" : "bot"}>
            {c.text}
          </div>
        ))}
        <div ref={chatEndRef}></div>
      </div>

      <div className="input-box">
        <input
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Type message..."
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              e.preventDefault();
              sendMessage();
            }
          }}
        />

        <button onClick={sendMessage}>Send</button>
        <button onClick={startListening}>🎤</button>
      </div>
    </div>
  );
}

export default App;