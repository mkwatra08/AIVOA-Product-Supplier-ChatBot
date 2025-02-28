from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from db import (
    fetch_suppliers, fetch_products, fetch_products_by_brand, fetch_suppliers_by_category,
    save_chat_message, get_chat_history
)
from chatbot import chatbot

# Initialize FastAPI
app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change for security)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# ✅ Test Endpoint
@app.get("/")
def home():
    return {"message": "AI Chatbot Backend is running!"}

# ✅ Fetch Suppliers
@app.get("/suppliers")
def get_suppliers():
    return {"suppliers": fetch_suppliers()}

# ✅ Fetch Products
@app.get("/products")
def get_products():
    return {"products": fetch_products()}

# ✅ Fetch Products by Brand
@app.get("/products/brand/{brand}")
def get_products_by_brand(brand: str):
    return {"products": fetch_products_by_brand(brand)}

# ✅ Fetch Suppliers by Category
@app.get("/suppliers/category/{category}")
def get_suppliers_by_category(category: str):
    return {"suppliers": fetch_suppliers_by_category(category)}

# ✅ Chat Request Model
class ChatRequest(BaseModel):
    user_message: str

# ✅ Chat Endpoint (Stores & Retrieves Chat History)
@app.post("/chat")
def chat(request: ChatRequest, http_request: Request):
    user_id = http_request.client.host  # Use user IP as a temporary identifier
    chat_history = get_chat_history(user_id)

    # Prepare the input with previous messages
    messages = [{"role": "user", "content": msg["message"]} for msg in chat_history]
    messages.append({"role": "user", "content": request.user_message})  # Add latest message

    state = {"messages": messages}
    new_state = chatbot.invoke(state)

    # ✅ Extract only the last assistant message
    chatbot_response = next(
        (msg["content"] for msg in new_state["messages"] if msg["role"] == "assistant"),
        "⚠ No response."
    )

    # ✅ Store chat in DB
    save_chat_message(user_id, request.user_message, chatbot_response)

    return {"response": chatbot_response}

# ✅ Get Chat History
@app.get("/chat/history")
def get_chat_history_api(request: Request):
    user_id = request.client.host  # Identify user by IP
    history = get_chat_history(user_id)

    if not history:
        return {"history": []}  # ✅ Return an empty array if no history

    formatted_history = [{"role": "user", "content": msg["message"]} for msg in history]
    return {"history": formatted_history}  # ✅ Ensure correct response format

