import React, { useState, useEffect } from "react";
import axios from "axios";

const API_URL = "http://127.0.0.1:8000";

const Chatbot = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");
    const [history, setHistory] = useState([]);
    const [showHistory, setShowHistory] = useState(false); // Toggle for history modal

    const handleChatSubmit = async () => {
        if (!input.trim()) return;

        setMessages(prevMessages => [...prevMessages, { role: "user", content: input }]);

        try {
            const response = await axios.post(`${API_URL}/chat`, { user_message: input });
            setMessages(prevMessages => [...prevMessages, { role: "bot", content: response.data.response }]);
        } catch (error) {
            console.error("Error connecting to chatbot:", error);
            setMessages(prevMessages => [...prevMessages, { role: "bot", content: "⚠ Error fetching response." }]);
        }

        setInput("");
    };

    const fetchChatHistory = async () => {
        try {
            console.log("📤 Fetching chat history...");
            const response = await axios.get(`${API_URL}/chat/history`);

            console.log("📥 Chat history API response:", response.data); // ✅ Debugging log

            if (response.data && response.data.history) {
                console.log("✅ Setting history:", response.data.history); // ✅ Ensure state update
                setHistory(response.data.history);
            } else {
                console.warn("⚠ No history found in response.");
                setHistory([]); // Avoid null values
            }
        } catch (error) {
            console.error("❌ Error fetching chat history:", error);
        }
    };

    return (
        <div style={{ padding: 20, maxWidth: 500, margin: "auto", fontFamily: "Arial, sans-serif" }}>
            <h2 style={{ textAlign: "center" }}>Chatbot</h2>
            <div style={{ border: "1px solid #ccc", padding: 10, height: 300, overflowY: "auto", background: "#f9f9f9", borderRadius: 8 }}>
                {messages.map((msg, index) => (
                    <div key={index} style={{ textAlign: msg.role === "user" ? "right" : "left", marginBottom: 10 }}>
                        <strong>{msg.role === "user" ? "You" : "Bot"}:</strong> {msg.content}
                    </div>
                ))}
            </div>
            <div style={{ display: "flex", marginTop: 10 }}>
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Type your message..."
                    style={{ flex: 1, padding: 10, borderRadius: 5, border: "1px solid #ccc", outline: "none" }}
                />
                <button onClick={handleChatSubmit} style={{ padding: "10px 15px", marginLeft: 10, background: "#007bff", color: "white", border: "none", borderRadius: 5, cursor: "pointer" }}>
                    Send
                </button>
                <button onClick={() => { fetchChatHistory(); setShowHistory(true); }} style={{ padding: "10px 15px", marginLeft: 5, background: "#28a745", color: "white", border: "none", borderRadius: 5, cursor: "pointer" }}>
                    📜 History
                </button>
            </div>

            {/* Chat History Modal */}
            {showHistory && (
                <div style={{
                    position: "fixed", top: "20%", left: "50%", transform: "translate(-50%, -50%)",
                    width: "350px", background: "white", padding: 15, borderRadius: 8, boxShadow: "0px 0px 10px rgba(0,0,0,0.2)", zIndex: 1000
                }}>
                    <h3 style={{ textAlign: "center" }}>Chat History</h3>
                    <div style={{ maxHeight: "300px", overflowY: "auto", padding: 10 }}>
                        {history.length > 0 ? (
                            history.map((msg, index) => (
                                <div key={index} style={{ marginBottom: 8 }}>
                                    <strong>{msg.role === "user" ? "You" : "Bot"}:</strong> {msg.content}
                                </div>
                            ))
                        ) : (
                            <p>⚠ No chat history available.</p>
                        )}
                    </div>
                    <button onClick={() => setShowHistory(false)} style={{
                        width: "100%", marginTop: 10, padding: 10, background: "#dc3545", color: "white",
                        border: "none", borderRadius: 5, cursor: "pointer"
                    }}>
                        Close
                    </button>
                </div>
            )}
        </div>
    );
};

export default Chatbot;
