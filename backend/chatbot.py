from langgraph.graph import StateGraph
from db import fetch_products_by_brand, fetch_suppliers_by_category
from llm import generate_gemini_response
from pydantic import BaseModel
from typing import List, Dict

class ChatState(BaseModel):
    messages: List[Dict[str, str]]

def classify_query(state: dict):
    last_message = state["messages"][-1]["content"].lower()

    # Improve product/supplier detection (avoid single-word misclassification)
    product_keywords = ["product", "brand", "price", "list of products"]
    supplier_keywords = ["supplier", "distributor", "manufacturer", "vendor"]

    # If the message contains specific product-related words
    if any(word in last_message for word in product_keywords):
        return {"next_node": "fetch_product", "messages": state["messages"]}

    # If the message contains supplier-related words but not general queries
    elif any(word in last_message for word in supplier_keywords) and len(last_message.split()) > 2:
        return {"next_node": "fetch_supplier", "messages": state["messages"]}

    # Default case: Treat it as a general query for Gemini AI
    else:
        return {"next_node": "generate_response", "messages": state["messages"]}


def fetch_product(state: dict):
    """Fetch products based on user query."""
    last_message = state["messages"][-1]["content"]
    brand = last_message.split()[-1].capitalize()  # Ensure case matching
    products = fetch_products_by_brand(brand)

    if products:
        product_list = "\n".join([f"- {p['name']} (${p['price']})" for p in products])
        response = f"Here are the products under {brand}:\n{product_list}"
    else:
        response = f"No products found under {brand}."

    print(f"✅ DEBUG: Response sent to chatbot: {response}")  # Debugging log

    # ✅ Fix: Return a dictionary instead of `ChatState`
    updated_messages = state["messages"] + [{"role": "assistant", "content": response}]
    return {"messages": updated_messages}  # ✅ Ensure chatbot can process the response




import re
def fetch_supplier(state: dict):
    """Fetch suppliers based on user query."""
    last_message = state["messages"][-1]["content"].lower().strip()

    # ✅ Improve category extraction by removing unnecessary words
    category = re.sub(r"[^a-zA-Z0-9 ]", "", last_message)  # Remove punctuation
    words_to_remove = ["who", "are", "the", "for", "suppliers", "provide", "that", "deals", "in"]
    
    # Remove common stopwords
    category_words = [word for word in category.split() if word not in words_to_remove]
    category = " ".join(category_words).strip()

    print(f"🔍 Extracted category: '{category}'")  # Debugging log

    # Fetch suppliers using cleaned category
    suppliers = fetch_suppliers_by_category(category)

    print(f"✅ Suppliers fetched: {suppliers}")  # Debugging log

    # ✅ Corrected response formatting
    if suppliers:
        supplier_list = "\n".join([f"- {s['name']} (Contact: {s['contact_info']})" for s in suppliers])
        response = f"Here are suppliers for {category}:\n{supplier_list}"
    else:
        response = f"No suppliers found for {category}."

    updated_messages = state["messages"] + [{"role": "assistant", "content": response}]
    return {"messages": updated_messages}  # ✅ Ensure chatbot can process response






def generate_response(state: dict):
    """Generate a response using Gemini AI."""
    last_message = state["messages"][-1]["content"]
    response = generate_gemini_response(last_message)
    
    updated_messages = state["messages"] + [{"role": "assistant", "content": response}]
    return {"messages": updated_messages}  # ✅ Ensure chatbot can process response


# Create LangGraph Workflow
workflow = StateGraph(dict)  # Use dict instead of ChatState
workflow.add_node("classify_query", classify_query)
workflow.add_node("fetch_product", fetch_product)
workflow.add_node("fetch_supplier", fetch_supplier)
workflow.add_node("generate_response", generate_response)

workflow.set_entry_point("classify_query")
workflow.add_conditional_edges(
    "classify_query",
    lambda state: state["next_node"],  # ✅ Use `state["next_node"]` instead of `.get()`
    {
        "fetch_product": "fetch_product",
        "fetch_supplier": "fetch_supplier",
        "generate_response": "generate_response"
    }
)

chatbot = workflow.compile()
