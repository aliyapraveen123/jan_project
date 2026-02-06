"""
Test AIService with Gemini API
"""

import os
import sys
from dotenv import load_dotenv

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

from backend.services.ai_service import AIService

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("ERROR: No API key found in .env file")
    exit(1)

print("Testing AIService with Gemini API...\n")

# Initialize service
ai_service = AIService(api_key)

# Test with sample transcript
test_transcript = """
This video explains photosynthesis. Plants use sunlight, water, and carbon dioxide to create glucose and oxygen.
The process occurs in chloroplasts. Chlorophyll is the green pigment that captures light energy.
The light-dependent reactions happen in the thylakoid membranes, while the Calvin cycle occurs in the stroma.
"""

print("1. Testing summary generation...")
try:
    summary = ai_service.generate_summary(test_transcript)
    if summary:
        print(f"✅ Summary generated ({len(summary)} chars)")
        print(f"Preview: {summary[:200]}...\n")
    else:
        print("❌ Summary generation failed\n")
except Exception as e:
    print(f"❌ Error: {e}\n")

print("2. Testing key points extraction...")
try:
    key_points = ai_service.extract_key_points(test_transcript)
    if key_points:
        print(f"✅ Key points extracted ({len(key_points)} chars)")
        print(f"Preview: {key_points[:200]}...\n")
    else:
        print("❌ Key points extraction failed\n")
except Exception as e:
    print(f"❌ Error: {e}\n")

print("3. Testing quiz generation...")
try:
    quiz = ai_service.generate_quiz(test_transcript)
    if quiz:
        print(f"✅ Quiz generated")
        print(f"Number of questions: {len(quiz)}\n")
    else:
        print("❌ Quiz generation failed\n")
except Exception as e:
    print(f"❌ Error: {e}\n")

print("=" * 50)
print("✅ All AIService tests completed!")
