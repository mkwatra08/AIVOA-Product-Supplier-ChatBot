import google.generativeai as genai

# Configure API Key
GEMINI_API_KEY = "AIzaSyCNQqPlGyLc_KDVFx07tdA_1vHUiap2pQw"  # Replace with your actual API key
genai.configure(api_key=GEMINI_API_KEY)

# List available models
available_models = genai.list_models()
print("✅ Available Gemini Models:")
for model in available_models:
    print(f"- {model.name}")
