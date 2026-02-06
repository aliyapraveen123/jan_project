"""
Main Streamlit UI Application - ChatGPT Style
Clean, minimal interface with no sidebar
ULTIMATE FREE MODE: Cache + Multi-Key Rotation + Caption-First + Smart Delays
"""

import streamlit as st
import sys
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from backend.services.transcript_service import TranscriptService
from backend.services.ai_service import AIService
from backend.utils.url_utils import URLUtils
from backend.utils.file_utils import FileUtils
from backend.utils.cache_manager import CacheManager
from backend.utils.api_key_rotator import APIKeyRotator


# Configure page - minimal layout
st.set_page_config(
    page_title="YouTube Learning Assistant",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Hide sidebar completely
st.markdown("""
<style>
    [data-testid="stSidebar"] {display: none;}
    .block-container {padding-top: 2rem;}
</style>
""", unsafe_allow_html=True)


def main():
    """Main application function - ChatGPT style interface"""
    
    # Initialize cache and key rotator
    cache = CacheManager()
    
    try:
        key_rotator = APIKeyRotator()
    except ValueError as e:
        st.error(f"⚠️ {str(e)}")
        st.info("Please add API keys to your .env file:\n"
                "```\n"
                "GOOGLE_API_KEY=your_key_1\n"
                "GOOGLE_API_KEY_2=your_key_2  # Optional\n"
                "GOOGLE_API_KEY_3=your_key_3  # Optional\n"
                "```")
        st.stop()
    
    # Load API key from rotator
    api_key = key_rotator.get_current_key()
    
    if not api_key:
        st.error("⚠️ All API keys exhausted for today")
        st.info("💡 **Free tier limits reached (20 requests/day per key)**\n\n"
                "Options:\n"
                "- Wait until tomorrow for quota reset\n"
                "- Add more API keys to .env file\n"
                "- Use cached results (see stats below)")
        
        # Show stats
        stats = key_rotator.get_stats()
        st.markdown("### 📊 API Usage Stats")
        for key_info in stats['keys']:
            st.write(f"**Key {key_info['key_number']}**: {key_info['requests_today']}/20 used today "
                    f"(Remaining: {key_info['remaining_today']})")
        
        cache_stats = cache.get_cache_stats()
        st.markdown("### 💾 Cache Stats")
        st.write(f"**Cached videos**: {cache_stats['total_videos']}")
        st.stop()
    
    # Minimal header
    st.title("🎓 YouTube Learning Assistant")
    st.caption("🚀 ULTIMATE FREE MODE: Multi-key rotation + Caching + Caption-first")
    
    # Show stats in expander
    with st.expander("📊 View Usage & Cache Stats"):
        stats = key_rotator.get_stats()
        st.markdown("#### API Keys Status")
        for key_info in stats['keys']:
            remaining = key_info['remaining_today']
            used = key_info['requests_today']
            progress = used / 20
            st.write(f"**Key {key_info['key_number']}**: {used}/20 requests used")
            st.progress(progress)
        
        cache_stats = cache.get_cache_stats()
        st.markdown("#### Cache Status")
        st.write(f"📦 **Cached videos**: {cache_stats['total_videos']}")
        st.write(f"✅ **Cache saves**: ~{cache_stats['total_videos'] * 4} API calls saved!")
    
    # Single input - ChatGPT style
    video_url = st.text_input(
        "Enter YouTube URL",
        placeholder="https://www.youtube.com/watch?v=...",
        label_visibility="collapsed"
    )
    
    # Process when URL is entered
    if video_url and video_url.strip():
        
        # Validate URL
        if not URLUtils.is_valid_youtube_url(video_url):
            st.error("❌ Invalid YouTube URL. Please check and try again.")
            st.stop()
        
        # Extract video ID
        video_id = URLUtils.extract_video_id(video_url)
        if not video_id:
            st.error("❌ Could not extract video ID from URL.")
            st.stop()
        
        # Show video
        st.video(video_url)
        
        # Check cache first
        cached_data = cache.get_cached_data(video_id)
        
        if cached_data:
            # Use cached data - NO API CALLS!
            st.success("⚡ Using cached data - 0 API calls used!")
            transcript = cached_data['transcript']
            summary = cached_data['summary']
            key_points = cached_data['key_points']
            quiz_data = cached_data['quiz']
        
        else:
            # Processing with status updates
            with st.status("🔍 Analyzing video...", expanded=True) as status:
                
                # Step 1: Check if we have available quota
                if not key_rotator.has_available_quota():
                    status.update(label="❌ Quota Exhausted", state="error")
                    st.error("All API keys exhausted for today. Please add more keys or wait until tomorrow.")
                    st.stop()
                
                # Step 2: Get transcript (caption-first, no API call if available)
                st.write("📥 Extracting transcript...")
                transcript_service = TranscriptService(api_key)
                transcript, _ = transcript_service.get_transcript(video_id)
                
                if not transcript:
                    status.update(label="❌ Failed", state="error")
                    st.error("Could not extract transcript from this video.")
                    st.info("💡 **Possible reasons:**\n"
                           "- Video may be age-restricted or private\n"
                           "- Audio download blocked (YouTube bot protection)\n"
                           "- API quota exceeded (free tier: 20 requests/day)\n"
                           "- Network connectivity issue\n\n"
                           "**✅ Best Solution:** Use videos with captions enabled\n"
                           "- Khan Academy, TED Talks, Coursera work perfectly!\n"
                           "- Captions = FREE + FAST (no API calls for transcription)\n\n"
                           "**⚠️ Note:** Audio transcription may not work on Streamlit Cloud due to YouTube's bot protection. "
                           "For videos without captions, consider running the app locally.")
                    st.stop()
                
                st.write(f"✅ Transcript extracted ({len(transcript.split())} words)")
                
                # Save transcript to cache
                cache.save_to_cache(video_id, transcript=transcript)
                
                # Step 3: Generate AI content with key rotation
                st.write("🤖 Generating AI summary...")
                
                # Get fresh key for each request
                current_key = key_rotator.get_next_key()
                if not current_key:
                    status.update(label="❌ Quota Exhausted", state="error")
                    st.error("API quota exhausted. Please wait until tomorrow.")
                    st.stop()
                
                ai_service = AIService(current_key)
                summary = ai_service.generate_summary(transcript)
                key_rotator.record_request(current_key)
                cache.save_to_cache(video_id, summary=summary)
                
                time.sleep(13)  # Wait 13 seconds (5 requests/min = 12s between requests + buffer)
                
                st.write("🎯 Extracting key points...")
                
                # Rotate to next key
                current_key = key_rotator.get_next_key()
                if not current_key:
                    st.warning("⚠️ Quota exhausted. Saving partial results to cache.")
                    key_points = None
                    quiz_data = None
                else:
                    ai_service.update_api_key(current_key)
                    key_points = ai_service.extract_key_points(transcript)
                    key_rotator.record_request(current_key)
                    cache.save_to_cache(video_id, key_points=key_points)
                    
                    time.sleep(13)  # Wait before quiz generation
                    
                    st.write("📊 Creating quiz...")
                    
                    # Rotate to next key
                    current_key = key_rotator.get_next_key()
                    if not current_key:
                        st.warning("⚠️ Quota exhausted. Saving partial results to cache.")
                        quiz_data = None
                    else:
                        ai_service.update_api_key(current_key)
                        quiz_data = ai_service.generate_quiz(transcript)
                        key_rotator.record_request(current_key)
                        cache.save_to_cache(video_id, quiz=quiz_data)
                
                status.update(label="✅ Analysis complete!", state="complete")
        
        # Display results - ChatGPT style streaming appearance
        st.markdown("---")
        
        # Summary
        st.markdown("### 📝 Summary")
        if summary:
            st.markdown(summary)
            st.download_button(
                "📥 Download Summary",
                summary,
                file_name=f"summary_{video_id}.txt",
                mime="text/plain"
            )
        
        st.markdown("---")
        
        # Key Points
        st.markdown("### 🎯 Key Learning Points")
        if key_points:
            st.markdown(key_points)
            st.download_button(
                "📥 Download Key Points",
                key_points,
                file_name=f"keypoints_{video_id}.txt",
                mime="text/plain"
            )
        
        st.markdown("---")
        
        # Quiz
        st.markdown("### 📊 Test Your Knowledge")
        if quiz_data:
            from frontend.components.quiz_component import display_quiz
            display_quiz(quiz_data)
        
        # Transcript (collapsible)
        with st.expander("📄 View Full Transcript"):
            st.text_area("", transcript, height=300, label_visibility="collapsed")
            st.download_button(
                "📥 Download Transcript",
                transcript,
                file_name=f"transcript_{video_id}.txt",
                mime="text/plain"
            )


if __name__ == "__main__":
    main()
