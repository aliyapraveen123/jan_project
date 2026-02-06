"""
Test script for Gemini-based transcript extraction
This demonstrates how to use Gemini AI to extract transcripts from YouTube videos
"""

import sys
import os
from backend.services.transcript_service import TranscriptService

def test_transcript_extraction():
    """Test transcript extraction with Gemini"""
    
    print("=" * 60)
    print("YouTube Transcript Extraction Test")
    print("=" * 60)
    print()
    
    # Get API key
    api_key = input("Enter your Google Gemini API Key: ").strip()
    if not api_key:
        print("❌ API key is required!")
        return
    
    # Get YouTube URL
    youtube_url = input("Enter YouTube video URL: ").strip()
    if not youtube_url:
        print("❌ YouTube URL is required!")
        return
    
    # Extract video ID
    from backend.utils.url_utils import URLUtils
    video_id = URLUtils.extract_video_id(youtube_url)
    if not video_id:
        print("❌ Could not extract video ID from URL")
        return
    
    print(f"\n✅ Video ID: {video_id}")
    print(f"📺 Processing: {youtube_url}")
    print()
    
    # Test with Gemini
    print("🤖 Testing Gemini AI transcript extraction...")
    print("-" * 60)
    transcript_service = TranscriptService(api_key=api_key, use_gemini=True)
    transcript, _ = transcript_service.get_transcript(video_id, youtube_url=youtube_url)
    
    if transcript:
        word_count = len(transcript.split())
        print(f"✅ Success! Extracted {word_count} words")
        print("\n📄 Transcript Preview (first 500 characters):")
        print("-" * 60)
        print(transcript[:500] + "...")
        print("-" * 60)
        
        # Save to file
        output_file = f"transcript_{video_id}.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(transcript)
        print(f"\n💾 Full transcript saved to: {output_file}")
    else:
        print("❌ Failed to extract transcript with Gemini")
        print("💡 Trying fallback method (Caption API)...")
        
        # Try traditional method
        transcript_service = TranscriptService(use_gemini=False)
        transcript, _ = transcript_service.get_transcript(video_id)
        
        if transcript:
            word_count = len(transcript.split())
            print(f"✅ Success with Caption API! Extracted {word_count} words")
            print("\n📄 Transcript Preview (first 500 characters):")
            print("-" * 60)
            print(transcript[:500] + "...")
            print("-" * 60)
        else:
            print("❌ Both methods failed. Video might not have captions or be accessible.")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    try:
        test_transcript_extraction()
    except KeyboardInterrupt:
        print("\n\n❌ Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
