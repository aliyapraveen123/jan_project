import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=api_key)

# Test different models to find one that works
models_to_test = [
    'gemini-1.5-flash',
    'gemini-1.5-flash-8b',
    'gemini-pro',
    'gemini-flash-latest',
]

print("🔍 Testing which models work with your API key...\n")

for model_name in models_to_test:
    try:
        print(f"Testing: {model_name}...")
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Say 'Hello' in one word")
        print(f"✅ SUCCESS: {model_name} works!")
        print(f"   Response: {response.text}\n")
        break
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "quota" in error_msg.lower():
            print(f"⚠️  QUOTA EXCEEDED: {model_name}")
        elif "404" in error_msg:
            print(f"❌ NOT FOUND: {model_name}")
        else:
            print(f"❌ ERROR: {model_name} - {error_msg[:100]}")
        print()

print("\n💡 Recommendation: Wait 1 minute, then your quota will reset.")
print("💡 Or create a new API key at: https://aistudio.google.com/app/apikey")
