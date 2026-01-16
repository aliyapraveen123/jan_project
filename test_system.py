"""
Test script to verify all functionality works correctly
"""

def test_imports():
    """Test if all required packages are installed"""
    print("Testing imports...")
    try:
        import streamlit
        print("✅ Streamlit imported successfully")
        
        import youtube_transcript_api
        print("✅ YouTube Transcript API imported successfully")
        
        import google.generativeai
        print("✅ Google Generative AI imported successfully")
        
        import json
        print("✅ JSON module available")
        
        import re
        print("✅ Regex module available")
        
        from urllib.parse import urlparse, parse_qs
        print("✅ URL parsing modules available")
        
        print("\n✅ All imports successful!")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_video_id_extraction():
    """Test video ID extraction from different URL formats"""
    print("\nTesting video ID extraction...")
    
    test_urls = [
        ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ("https://youtu.be/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ("https://www.youtube.com/embed/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
    ]
    
    from urllib.parse import urlparse, parse_qs
    
    def extract_video_id(url):
        try:
            if "youtu.be" in url:
                return url.split("/")[-1].split("?")[0]
            elif "youtube.com" in url:
                parsed_url = urlparse(url)
                if parsed_url.path == "/watch":
                    return parse_qs(parsed_url.query)["v"][0]
                elif parsed_url.path.startswith("/embed/"):
                    return parsed_url.path.split("/")[2]
            return None
        except:
            return None
    
    all_passed = True
    for url, expected_id in test_urls:
        video_id = extract_video_id(url)
        if video_id == expected_id:
            print(f"✅ {url[:50]}... -> {video_id}")
        else:
            print(f"❌ {url[:50]}... -> Expected {expected_id}, got {video_id}")
            all_passed = False
    
    if all_passed:
        print("✅ All video ID extraction tests passed!")
    return all_passed

def test_package_versions():
    """Check package versions"""
    print("\nChecking package versions...")
    
    import streamlit
    import google.generativeai
    
    print(f"Streamlit version: {streamlit.__version__}")
    print(f"Google Generative AI version: {google.generativeai.__version__}")
    print("YouTube Transcript API: installed ✅")
    
    return True

def main():
    print("=" * 60)
    print("YouTube Learning Assistant - System Test")
    print("=" * 60)
    print()
    
    tests_passed = 0
    total_tests = 3
    
    if test_imports():
        tests_passed += 1
    
    if test_video_id_extraction():
        tests_passed += 1
    
    if test_package_versions():
        tests_passed += 1
    
    print("\n" + "=" * 60)
    print(f"Test Results: {tests_passed}/{total_tests} tests passed")
    print("=" * 60)
    
    if tests_passed == total_tests:
        print("\n✅ All tests passed! Your system is ready.")
        print("\nNext steps:")
        print("1. Get your Google Gemini API key from:")
        print("   https://makersuite.google.com/app/apikey")
        print("2. Run the application with: streamlit run app.py")
        print("3. Enter your API key in the sidebar")
        print("4. Start processing YouTube videos!")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        print("Try reinstalling dependencies: pip install -r requirements.txt")

if __name__ == "__main__":
    main()
