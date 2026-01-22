import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv('GOOGLE_API_KEY')
print(f"API Key: {api_key[:10]}...{api_key[-5:]}")

# Configure API
genai.configure(api_key=api_key)

# List available models
print("\n🔍 Available Gemini Models:")
print("-" * 60)

for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"✅ {model.name}")
        print(f"   Display Name: {model.display_name}")
        print(f"   Description: {model.description}")
        print()

print("\n🧪 Testing model with simple prompt...")
try:
    # Try gemini-1.5-flash
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Say hello")
    print("✅ SUCCESS with gemini-1.5-flash!")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"❌ FAILED with gemini-1.5-flash: {e}")
    
    # Try alternative model
    try:
        print("\n🔄 Trying models/gemini-1.5-flash...")
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        response = model.generate_content("Say hello")
        print("✅ SUCCESS with models/gemini-1.5-flash!")
        print(f"Response: {response.text}")
    except Exception as e2:
        print(f"❌ FAILED: {e2}")
