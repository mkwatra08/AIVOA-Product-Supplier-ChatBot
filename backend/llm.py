import google.generativeai as genai

# Configure Gemini API
GEMINI_API_KEY = "AIzaSyCNQqPlGyLc_KDVFx07tdA_1vHUiap2pQw"  # Replace with your actual API key
genai.configure(api_key=GEMINI_API_KEY)

def generate_gemini_response(prompt: str) -> str:
    """Fetch response from Gemini AI model."""
    try:
        model = genai.GenerativeModel("models/gemini-1.5-pro")  # ✅ Use correct model name
        response = model.generate_content(prompt)

        if response and hasattr(response, "text"):
            return response.text.strip()
        else:
            return "Sorry, I couldn't generate a response."

    except Exception as e:
        print(f"❌ Error in Gemini API: {e}")  # Print the full error for debugging
        return f"Error in generating response from Gemini AI: {e}"
