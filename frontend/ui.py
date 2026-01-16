"""
Main Streamlit UI Application
Frontend interface for YouTube Learning Assistant
"""

import streamlit as st
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.services.transcript_service import TranscriptService
from backend.services.ai_service import AIService
from backend.utils.url_utils import URLUtils
from backend.utils.file_utils import FileUtils


# Configure page
st.set_page_config(
    page_title="YouTube Learning Assistant",
    page_icon="🎓",
    layout="wide"
)


def main():
    """Main application function"""
    # Title and description
    st.title("🎓 YouTube Learning Assistant")
    st.markdown("""
    Transform any YouTube educational video into structured learning content with:
    - 📄 Automatic transcript extraction
    - 📝 AI-generated summaries
    - 🎯 Key learning points
    - 📊 Interactive quizzes (10 questions)
    """)
    
    # Sidebar for API key
    with st.sidebar:
        st.header("⚙️ Configuration")
        api_key = st.text_input("Enter Google Gemini API Key", type="password")
        st.markdown("""
        **Don't have an API key?**
        
        Get a free API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
        """)
        
        st.markdown("---")
        st.markdown("### 📖 How to Use")
        st.markdown("""
        1. Enter your Gemini API key
        2. Paste a YouTube video URL
        3. Click 'Process Video'
        4. Explore the generated content:
           - Read the summary
           - Study key points
           - Take the quiz!
        """)
    
    # Main content area
    if not api_key:
        st.warning("⚠️ Please enter your Google Gemini API key in the sidebar to get started.")
        return
    
    # Video URL input
    video_url = st.text_input("🔗 Enter YouTube Video URL:", placeholder="https://www.youtube.com/watch?v=...")
    
    if st.button("🚀 Process Video", type="primary"):
        if not video_url:
            st.error("Please enter a YouTube video URL")
            return
        
        # Validate URL
        if not URLUtils.is_valid_youtube_url(video_url):
            st.error("Invalid YouTube URL. Please check and try again.")
            return
        
        # Extract video ID
        video_id = URLUtils.extract_video_id(video_url)
        if not video_id:
            st.error("Could not extract video ID from URL.")
            return
        
        # Show video
        st.video(video_url)
        
        # Get transcript
        with st.spinner("📥 Fetching video transcript..."):
            transcript_service = TranscriptService()
            transcript, transcript_list = transcript_service.get_transcript(video_id)
        
        if not transcript:
            st.error("Could not fetch transcript. Make sure the video has captions enabled.")
            st.info("""
            **Tips:**
            - Try videos from Khan Academy, TED-Ed, or freeCodeCamp
            - Check if video has CC (Closed Captions) button
            - Try with mobile hotspot if on restricted network
            """)
            return
        
        st.success(f"✅ Transcript extracted successfully! ({len(transcript.split())} words)")
        
        # Store in session state
        st.session_state.transcript = transcript
        st.session_state.video_id = video_id
        
        # Initialize AI service
        ai_service = AIService(api_key)
        
        # Create tabs for different features
        tab1, tab2, tab3, tab4 = st.tabs([
            "📄 Transcript", 
            "📝 Summary", 
            "🎯 Key Points", 
            "📊 Quiz"
        ])
        
        # Tab 1: Transcript
        with tab1:
            st.subheader("📄 Full Transcript")
            with st.expander("View Full Transcript", expanded=False):
                st.text_area("Transcript", transcript, height=400)
            
            # Download transcript
            filename = FileUtils.generate_filename("transcript", video_id, "txt")
            st.download_button(
                label="📥 Download Transcript",
                data=transcript,
                file_name=filename,
                mime="text/plain"
            )
        
        # Tab 2: Summary
        with tab2:
            with st.spinner("🤖 Generating comprehensive summary..."):
                summary = ai_service.generate_summary(transcript)
            
            if summary:
                st.subheader("📝 Video Summary")
                st.markdown(summary)
                
                # Download summary
                filename = FileUtils.generate_filename("summary", video_id, "txt")
                st.download_button(
                    label="📥 Download Summary",
                    data=summary,
                    file_name=filename,
                    mime="text/plain"
                )
        
        # Tab 3: Key Points
        with tab3:
            with st.spinner("🎯 Extracting key learning points..."):
                key_points = ai_service.extract_key_points(transcript)
            
            if key_points:
                st.subheader("🎯 Core Learning Points")
                st.markdown(key_points)
                
                # Download key points
                filename = FileUtils.generate_filename("keypoints", video_id, "txt")
                st.download_button(
                    label="📥 Download Key Points",
                    data=key_points,
                    file_name=filename,
                    mime="text/plain"
                )
        
        # Tab 4: Quiz
        with tab4:
            with st.spinner("📊 Generating 10 quiz questions from transcript..."):
                quiz_data = ai_service.generate_quiz(transcript)
            
            if quiz_data:
                from frontend.components.quiz_component import display_quiz
                display_quiz(quiz_data)
                
                # Download quiz
                quiz_json = FileUtils.format_quiz_json(quiz_data)
                filename = FileUtils.generate_filename("quiz", video_id, "json")
                st.download_button(
                    label="📥 Download Quiz (JSON)",
                    data=quiz_json,
                    file_name=filename,
                    mime="application/json"
                )


if __name__ == "__main__":
    main()
