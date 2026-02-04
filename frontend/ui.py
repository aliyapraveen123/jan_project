"""
Main Streamlit UI Application - ChatGPT Style
Clean, minimal interface with no sidebar
"""

import streamlit as st
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from backend.services.transcript_service import TranscriptService
from backend.services.ai_service import AIService
from backend.utils.url_utils import URLUtils
from backend.utils.file_utils import FileUtils


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
    
    # Load API key from environment
    api_key = os.getenv("GOOGLE_API_KEY", "")
    
    if not api_key:
        st.error("⚠️ API Key not found in .env file")
        st.info("Please add GOOGLE_API_KEY to your .env file")
        st.code("GOOGLE_API_KEY=your_key_here", language="bash")
        st.stop()
    
    # Minimal header
    st.title("🎓 YouTube Learning Assistant")
    st.caption("Paste a YouTube URL to get AI-powered summary, key points, and quiz")
    
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
        
        # Processing with status updates
        with st.status("🔍 Analyzing video...", expanded=True) as status:
            
            # Step 1: Get transcript
            st.write("📥 Extracting transcript...")
            transcript_service = TranscriptService(api_key)
            transcript, _ = transcript_service.get_transcript(video_id)
            
            if not transcript:
                status.update(label="❌ Failed", state="error")
                st.error("Could not extract transcript from this video.")
                st.info("💡 **Possible reasons:**\n"
                       "- Video may be age-restricted or private\n"
                       "- API quota exceeded (free tier: 20 requests/day)\n"
                       "- Network connectivity issue\n\n"
                       "**Try:** Videos with captions enabled (Khan Academy, TED, Coursera)")
                st.stop()
            
            st.write(f"✅ Transcript extracted ({len(transcript.split())} words)")
            
            # Step 2: Generate AI content
            ai_service = AIService(api_key)
            
            st.write("🤖 Generating AI summary...")
            summary = ai_service.generate_summary(transcript)
            
            st.write("🎯 Extracting key points...")
            key_points = ai_service.extract_key_points(transcript)
            
            st.write("📊 Creating quiz...")
            quiz_data = ai_service.generate_quiz(transcript)
            
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
