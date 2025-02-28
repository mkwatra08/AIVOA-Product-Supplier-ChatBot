import axios from "axios";

const API_URL = "http://127.0.0.1:8000";  // ✅ FastAPI backend URL

export const sendMessageToChatbot = async (message) => {
  try {
    console.log("📤 Sending message to chatbot:", message);  // Log user input

    const response = await axios.post(`${API_URL}/chat`, { user_message: message });

    console.log("📥 Chatbot API raw response:", response.data);  // Log API response

    return response.data.response?.trim() || "⚠ No valid response received.";
  } catch (error) {
    console.error("❌ Error in chatbot API:", error);
    return "Error connecting to chatbot.";
  }
};

