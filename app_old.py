import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
import google.generativeai as genai
import json
import re
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="YouTube Learning Assistant",
    page_icon="🎓",
    layout="wide"
)

# Configure Gemini API
def configure_gemini(api_key):
    """Configure Google Gemini API"""
    try:
        genai.configure(api_key=api_key)
        return True
    except Exception as e:
        st.error(f"Error configuring API: {str(e)}")
        return False

def extract_video_id(url):
    """Extract video ID from YouTube URL"""
    try:
        # Handle different YouTube URL formats
        if "youtu.be" in url:
            return url.split("/")[-1].split("?")[0]
        elif "youtube.com" in url:
            parsed_url = urlparse(url)
            if parsed_url.path == "/watch":
                return parse_qs(parsed_url.query)["v"][0]
            elif parsed_url.path.startswith("/embed/"):
                return parsed_url.path.split("/")[2]
            elif parsed_url.path.startswith("/v/"):
                return parsed_url.path.split("/")[2]
        return None
    except Exception as e:
        st.error(f"Error extracting video ID: {str(e)}")
        return None

def get_transcript(video_id):
    """Get transcript from YouTube video"""
    try:
        # Try to get transcript in multiple languages
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        # Try to get English transcript first
        try:
            transcript = transcript_list.find_transcript(['en'])
            transcript_data = transcript.fetch()
        except:
            # If English not available, get any available transcript
            try:
                transcript = transcript_list.find_generated_transcript(['en'])
                transcript_data = transcript.fetch()
            except:
                # Get the first available transcript in any language
                available_transcripts = list(transcript_list)
                if available_transcripts:
                    transcript_data = available_transcripts[0].fetch()
                else:
                    raise Exception("No transcripts available for this video")
        
        transcript_text = " ".join([item["text"] for item in transcript_data])
        return transcript_text, transcript_data
        
    except Exception as e:
        st.error(f"Error fetching transcript: {str(e)}")
        st.warning("⚠️ This video doesn't have accessible captions/subtitles.")
        st.info("""
        **Possible reasons:**
        - Video has no captions enabled
        - Captions are disabled by uploader
        - Video is age-restricted or private
        - Network/API temporary issue
        
        **Try these solutions:**
        1. Try a different video (Khan Academy, TED-Ed work well)
        2. Make sure video is public and has CC button
        3. Wait a moment and try again
        """)
        return None, None

def generate_summary(transcript, api_key):
    """Generate comprehensive summary using Gemini"""
    try:
        configure_gemini(api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"""
        You are an expert educational content analyzer. Analyze the following YouTube video transcript and provide a comprehensive summary.
        
        Transcript:
        {transcript}
        
        Please provide:
        1. A brief overview (2-3 sentences)
        2. Main topics covered (bullet points)
        3. Detailed summary organized by sections
        4. Key takeaways
        
        Format your response in a clear, structured way suitable for students.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error generating summary: {str(e)}")
        return None

def extract_key_points(transcript, api_key):
    """Extract core learning points from transcript"""
    try:
        configure_gemini(api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"""
        You are an expert educator. Analyze the following YouTube video transcript and extract the most important learning points.
        
        Transcript:
        {transcript}
        
        Extract 8-12 core learning points that students MUST remember. These should be:
        - Factual and specific
        - Exam-oriented
        - Clear and concise
        - Cover all major concepts
        
        Format each point as a numbered list with brief explanations where needed.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error extracting key points: {str(e)}")
        return None

def generate_quiz(transcript, api_key):
    """Generate exactly 10 quiz questions from transcript"""
    try:
        configure_gemini(api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"""
        You are an expert quiz creator. Based on the following YouTube video transcript, create EXACTLY 10 multiple-choice questions.
        
        Transcript:
        {transcript}
        
        Requirements:
        - Create EXACTLY 10 questions (no more, no less)
        - Questions should test understanding of key concepts from the video
        - Each question must have 4 options (A, B, C, D)
        - Only ONE correct answer per question
        - Include a mix of difficulty levels (easy, medium, hard)
        - Questions should be clear and unambiguous
        
        Format your response as a JSON array with this structure:
        [
            {{
                "question": "Question text here?",
                "options": {{
                    "A": "Option A text",
                    "B": "Option B text",
                    "C": "Option C text",
                    "D": "Option D text"
                }},
                "correct_answer": "A",
                "explanation": "Brief explanation of why this is correct"
            }}
        ]
        
        Return ONLY the JSON array, nothing else.
        """
        
        response = model.generate_content(prompt)
        quiz_text = response.text.strip()
        
        # Extract JSON from response
        json_match = re.search(r'\[.*\]', quiz_text, re.DOTALL)
        if json_match:
            quiz_json = json_match.group(0)
            quiz_data = json.loads(quiz_json)
            
            # Ensure exactly 10 questions
            if len(quiz_data) > 10:
                quiz_data = quiz_data[:10]
            elif len(quiz_data) < 10:
                st.warning(f"Generated {len(quiz_data)} questions instead of 10. Regenerating...")
                return generate_quiz(transcript, api_key)
            
            return quiz_data
        else:
            st.error("Could not parse quiz JSON")
            return None
            
    except json.JSONDecodeError as e:
        st.error(f"Error parsing quiz JSON: {str(e)}")
        return None
    except Exception as e:
        st.error(f"Error generating quiz: {str(e)}")
        return None

def display_quiz(quiz_data):
    """Display interactive quiz"""
    if not quiz_data or len(quiz_data) == 0:
        st.error("No quiz data available")
        return
    
    st.subheader(f"📝 Quiz ({len(quiz_data)} Questions)")
    
    if 'quiz_answers' not in st.session_state:
        st.session_state.quiz_answers = {}
    if 'quiz_submitted' not in st.session_state:
        st.session_state.quiz_submitted = False
    
    # Display questions
    for i, q in enumerate(quiz_data, 1):
        st.markdown(f"**Question {i}:** {q['question']}")
        
        options = q['options']
        answer = st.radio(
            f"Select your answer for Question {i}:",
            options=list(options.keys()),
            format_func=lambda x: f"{x}: {options[x]}",
            key=f"q_{i}",
            disabled=st.session_state.quiz_submitted
        )
        
        st.session_state.quiz_answers[i] = answer
        st.markdown("---")
    
    # Submit button
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        if st.button("Submit Quiz", type="primary"):
            st.session_state.quiz_submitted = True
            st.rerun()
    
    with col2:
        if st.button("Reset Quiz"):
            st.session_state.quiz_answers = {}
            st.session_state.quiz_submitted = False
            st.rerun()
    
    # Show results after submission
    if st.session_state.quiz_submitted:
        st.markdown("---")
        st.subheader("📊 Quiz Results")
        
        correct_count = 0
        for i, q in enumerate(quiz_data, 1):
            user_answer = st.session_state.quiz_answers.get(i)
            correct_answer = q['correct_answer']
            
            if user_answer == correct_answer:
                correct_count += 1
                st.success(f"✅ Question {i}: Correct!")
            else:
                st.error(f"❌ Question {i}: Incorrect")
                st.info(f"Your answer: {user_answer} | Correct answer: {correct_answer}")
            
            with st.expander(f"Explanation for Question {i}"):
                st.write(q.get('explanation', 'No explanation available'))
        
        # Overall score
        score_percentage = (correct_count / len(quiz_data)) * 100
        st.markdown("---")
        st.metric(
            "Your Score",
            f"{correct_count}/{len(quiz_data)}",
            f"{score_percentage:.1f}%"
        )
        
        # Performance feedback
        if score_percentage >= 80:
            st.success("🎉 Excellent! You have a strong understanding of the content!")
        elif score_percentage >= 60:
            st.info("👍 Good job! Review the missed questions to improve further.")
        else:
            st.warning("📚 Keep studying! Review the key points and try again.")

def main():
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
        
        video_id = extract_video_id(video_url)
        if not video_id:
            st.error("Invalid YouTube URL. Please check and try again.")
            return
        
        # Show video
        st.video(video_url)
        
        # Get transcript
        with st.spinner("📥 Fetching video transcript..."):
            transcript, transcript_list = get_transcript(video_id)
        
        if not transcript:
            st.error("Could not fetch transcript. Make sure the video has captions enabled.")
            return
        
        st.success(f"✅ Transcript extracted successfully! ({len(transcript.split())} words)")
        
        # Store in session state
        st.session_state.transcript = transcript
        st.session_state.video_id = video_id
        
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
            st.download_button(
                label="📥 Download Transcript",
                data=transcript,
                file_name=f"transcript_{video_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
        
        # Tab 2: Summary
        with tab2:
            with st.spinner("🤖 Generating comprehensive summary..."):
                summary = generate_summary(transcript, api_key)
            
            if summary:
                st.subheader("📝 Video Summary")
                st.markdown(summary)
                
                # Download summary
                st.download_button(
                    label="📥 Download Summary",
                    data=summary,
                    file_name=f"summary_{video_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
        
        # Tab 3: Key Points
        with tab3:
            with st.spinner("🎯 Extracting key learning points..."):
                key_points = extract_key_points(transcript, api_key)
            
            if key_points:
                st.subheader("🎯 Core Learning Points")
                st.markdown(key_points)
                
                # Download key points
                st.download_button(
                    label="📥 Download Key Points",
                    data=key_points,
                    file_name=f"keypoints_{video_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
        
        # Tab 4: Quiz
        with tab4:
            with st.spinner("📊 Generating 10 quiz questions from transcript..."):
                quiz_data = generate_quiz(transcript, api_key)
            
            if quiz_data:
                display_quiz(quiz_data)
                
                # Download quiz
                quiz_json = json.dumps(quiz_data, indent=2)
                st.download_button(
                    label="📥 Download Quiz (JSON)",
                    data=quiz_json,
                    file_name=f"quiz_{video_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )

if __name__ == "__main__":
    main()
