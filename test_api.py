"""
Test Gemini API configuration
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("GOOGLE_API_KEY")

print(f"API Key loaded: {api_key[:20]}..." if api_key else "API Key NOT found")

if not api_key:
    print("ERROR: No API key found in .env file")
    exit(1)

# Try to configure and test Gemini
try:
    print("\nConfiguring Gemini API...")
    genai.configure(api_key=api_key)
    
    print("Testing model initialization...")
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    print("Sending test prompt...")
    response = model.generate_content("Say 'Hello, API is working!'")
    
    print(f"\n✅ SUCCESS! Response: {response.text}")
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    print(f"Error type: {type(e).__name__}")
