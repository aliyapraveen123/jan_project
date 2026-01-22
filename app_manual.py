import streamlit as st
import google.generativeai as genai
import json
import re
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import hashlib
import time

# Load environment variables from .env file
load_dotenv()

# Initialize session state for quota management
if 'quota_exceeded_until' not in st.session_state:
    st.session_state.quota_exceeded_until = None
if 'api_call_count' not in st.session_state:
    st.session_state.api_call_count = 0
if 'processing' not in st.session_state:
    st.session_state.processing = False

# Configure page
st.set_page_config(
    page_title="YouTube Learning Assistant (Manual Mode)",
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

# Quota management functions
def is_quota_exceeded():
    """Check if we're currently in quota exceeded state"""
    if st.session_state.quota_exceeded_until:
        if datetime.now() < st.session_state.quota_exceeded_until:
            return True
        else:
            # Quota cooldown has passed
            st.session_state.quota_exceeded_until = None
            return False
    return False

def extract_retry_delay(error_message):
    """Extract retry delay from Gemini error response"""
    try:
        # Look for "retry in XXs" or "retry_delay { seconds: XX }"
        match = re.search(r'retry in (\d+(?:\.\d+)?)\s*s', str(error_message))
        if match:
            return float(match.group(1))
        
        match = re.search(r'seconds:\s*(\d+)', str(error_message))
        if match:
            return float(match.group(1))
        
        # Default to 60 seconds if not found
        return 60
    except:
        return 60

def handle_quota_error(error):
    """Handle quota exceeded error gracefully"""
    error_str = str(error)
    
    # Extract retry delay
    retry_seconds = extract_retry_delay(error_str)
    
    # Set quota exceeded state
    st.session_state.quota_exceeded_until = datetime.now() + timedelta(seconds=retry_seconds)
    
    return {
        'success': False,
        'reason': 'QUOTA_EXCEEDED',
        'retry_after': retry_seconds,
        'retry_at': st.session_state.quota_exceeded_until.strftime('%H:%M:%S'),
        'message': f'⚠️ Gemini API quota exceeded. Please wait {int(retry_seconds)} seconds.'
    }

def log_api_call(feature_name, success=True, cached=False):
    """Log API calls for debugging"""
    st.session_state.api_call_count += 1
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    status = "CACHED" if cached else ("SUCCESS" if success else "FAILED")
    
    # Store in session state for display
    if 'api_logs' not in st.session_state:
        st.session_state.api_logs = []
    
    st.session_state.api_logs.append({
        'timestamp': timestamp,
        'feature': feature_name,
        'status': status,
        'count': st.session_state.api_call_count
    })
    
    # Keep only last 20 logs
    if len(st.session_state.api_logs) > 20:
        st.session_state.api_logs = st.session_state.api_logs[-20:]

def call_gemini_with_protection(func, *args, **kwargs):
    """Wrapper to protect Gemini API calls with quota management"""
    # Check if quota is exceeded
    if is_quota_exceeded():
        time_left = (st.session_state.quota_exceeded_until - datetime.now()).total_seconds()
        return {
            'success': False,
            'reason': 'QUOTA_EXCEEDED',
            'retry_after': int(time_left),
            'retry_at': st.session_state.quota_exceeded_until.strftime('%H:%M:%S'),
            'message': f'⚠️ Still in cooldown. Wait {int(time_left)} more seconds.'
        }
    
    # Check if already processing (prevent double calls)
    if st.session_state.processing:
        return {
            'success': False,
            'reason': 'ALREADY_PROCESSING',
            'message': '⏳ Already processing a request. Please wait...'
        }
    
    try:
        st.session_state.processing = True
        result = func(*args, **kwargs)
        st.session_state.processing = False
        return {'success': True, 'data': result}
    
    except Exception as e:
        st.session_state.processing = False
        error_str = str(e)
        
        # Check if it's a quota error (429)
        if '429' in error_str or 'quota' in error_str.lower():
            return handle_quota_error(e)
        
        # Other errors
        return {
            'success': False,
            'reason': 'API_ERROR',
            'message': f'❌ Error: {error_str[:200]}'
        }

# Cache helper function
def get_cache_key(transcript):
    """Generate unique cache key for transcript"""
    return hashlib.md5(transcript.encode()).hexdigest()

@st.cache_data(ttl=3600)  # Cache for 1 hour
def generate_summary_cached(transcript, api_key, cache_key):
    """Generate comprehensive summary using Gemini (with caching)"""
    return generate_summary(transcript, api_key)

@st.cache_data(ttl=3600)  # Cache for 1 hour
def extract_key_points_cached(transcript, api_key, cache_key):
    """Extract key learning points (with caching)"""
    return extract_key_points(transcript, api_key)

@st.cache_data(ttl=3600)  # Cache for 1 hour
def generate_quiz_cached(transcript, api_key, cache_key):
    """Generate quiz questions (with caching)"""
    return generate_quiz(transcript, api_key)

def generate_summary(transcript, api_key):
    """Generate comprehensive summary using Gemini"""
    try:
        configure_gemini(api_key)
        model = genai.GenerativeModel('gemini-flash-latest')
        
        prompt = f"""
        You are an expert educational content analyzer. Analyze the following video transcript and provide a comprehensive summary.
        
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
        model = genai.GenerativeModel('gemini-flash-latest')
        
        prompt = f"""
        You are an expert educator. Analyze the following video transcript and extract the most important learning points.
        
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
        model = genai.GenerativeModel('gemini-flash-latest')
        
        prompt = f"""
        You are an expert quiz creator. Based on the following video transcript, create EXACTLY 10 multiple-choice questions.
        
        Transcript:
        {transcript}
        
        Requirements:
        - Create EXACTLY 10 questions (no more, no less)
        - Questions should test understanding of key concepts from the video
        - Each question must have 4 options (A, B, C, D)
        - Only ONE correct answer per question
        - Include a mix of difficulty levels (easy, medium, hard)
        - Questions should be clear and unambiguous
        - Do NOT use special characters or escape sequences in text
        
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
        
        Return ONLY the JSON array, nothing else. Make sure all text is properly escaped for JSON.
        """
        
        response = model.generate_content(prompt)
        quiz_text = response.text.strip()
        
        # Remove markdown code blocks if present
        quiz_text = re.sub(r'```json\s*', '', quiz_text)
        quiz_text = re.sub(r'```\s*', '', quiz_text)
        
        # Extract JSON from response
        json_match = re.search(r'\[.*\]', quiz_text, re.DOTALL)
        if json_match:
            quiz_json = json_match.group(0)
            
            # Fix common JSON escape issues
            # Replace invalid escape sequences with safe alternatives
            quiz_json = quiz_json.replace('\\/', '/')  # Forward slash doesn't need escaping
            quiz_json = quiz_json.replace('\\"', '"')  # Fix double-escaped quotes
            
            # Remove any other invalid escape sequences by replacing backslash followed by non-standard escape chars
            # Keep only valid JSON escapes: \", \\, \/, \b, \f, \n, \r, \t, \uXXXX
            import re
            def fix_escapes(match):
                escaped_char = match.group(1)
                if escaped_char in ['"', '\\', '/', 'b', 'f', 'n', 'r', 't']:
                    return match.group(0)  # Valid escape, keep it
                elif escaped_char == 'u':
                    return match.group(0)  # Unicode escape, keep it
                else:
                    return escaped_char  # Invalid escape, remove backslash
            
            quiz_json = re.sub(r'\\(.)', fix_escapes, quiz_json)
            
            try:
                quiz_data = json.loads(quiz_json)
            except json.JSONDecodeError as e:
                # If still failing, try a more aggressive cleanup
                st.warning("Cleaning up JSON formatting issues...")
                # Replace problematic characters
                quiz_json = quiz_json.replace('\n', ' ').replace('\r', ' ')
                quiz_json = re.sub(r'\s+', ' ', quiz_json)  # Normalize whitespace
                quiz_data = json.loads(quiz_json)
            
            # Ensure exactly 10 questions
            if len(quiz_data) > 10:
                quiz_data = quiz_data[:10]
            elif len(quiz_data) < 10:
                st.warning(f"Generated {len(quiz_data)} questions instead of 10. Using what we have...")
                # Don't regenerate to avoid infinite loop, just use what we got
            
            return quiz_data
        else:
            st.error("Could not find JSON array in response")
            return None
            
    except json.JSONDecodeError as e:
        st.error(f"Error parsing quiz JSON: {str(e)}")
        # Log the problematic JSON for debugging
        try:
            with open('jan_project_debug.log', 'a') as _dbg:
                _dbg.write(f"[{datetime.now().isoformat()}] Quiz JSON parse error: {str(e)}\n")
                _dbg.write(f"Problematic JSON snippet: {quiz_json[:500] if 'quiz_json' in locals() else 'N/A'}\n")
        except Exception:
            pass
        return None
    except Exception as e:
        st.error(f"Error generating quiz: {str(e)}")
        try:
            with open('jan_project_debug.log', 'a') as _dbg:
                _dbg.write(f"[{datetime.now().isoformat()}] Quiz generation error: {str(e)[:200]}\n")
        except Exception:
            pass
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
    st.title("🎓 YouTube Learning Assistant (Manual Mode)")
    st.markdown("""
    **Network Issue Workaround:** This version works without YouTube API access!
    
    Transform any YouTube video transcript into structured learning content with:
    - 📝 AI-generated summaries
    - 🎯 Key learning points
    - 📊 Interactive quizzes (10 questions)
    """)
    
    # Sidebar for API key
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Try to get API key from environment variable first
        default_api_key = os.getenv('GOOGLE_API_KEY', '')
        
        if default_api_key:
            st.success("✅ API Key loaded from .env file")
            api_key = default_api_key
            # Show masked version
            masked_key = default_api_key[:8] + "..." + default_api_key[-4:]
            st.code(masked_key)
        else:
            st.warning("⚠️ No API key found in .env file")
            api_key = st.text_input("Enter Google Gemini API Key", type="password")
        
        st.markdown("---")
        
        # Quota Status Display
        st.markdown("### 📊 API Status")
        if is_quota_exceeded():
            time_left = (st.session_state.quota_exceeded_until - datetime.now()).total_seconds()
            st.error(f"🚫 Quota Exceeded")
            st.info(f"⏳ Cooldown: {int(time_left)}s")
            st.caption(f"Ready at: {st.session_state.quota_exceeded_until.strftime('%H:%M:%S')}")
        else:
            st.success("✅ API Ready")
        
        st.metric("API Calls Made", st.session_state.api_call_count)
        
        # Show recent API logs
        if 'api_logs' in st.session_state and st.session_state.api_logs:
            with st.expander("📜 Recent API Calls"):
                for log in reversed(st.session_state.api_logs[-5:]):
                    status_icon = "✅" if log['status'] == "SUCCESS" else ("⚡" if log['status'] == "CACHED" else "❌")
                    st.caption(f"{status_icon} {log['feature']} - {log['timestamp']}")
        
        st.markdown("---")
        st.markdown("### 📖 How to Use")
        st.markdown("""
        **Since YouTube API is blocked on your network:**
        
        1. Open the YouTube video
        2. Click "..." menu (below video)
        3. Click "Show transcript"
        4. Copy ALL the transcript text
        5. Paste it below
        6. Click "Process Transcript"
        """)
        
        st.markdown("---")
        st.markdown("### 🎬 Video Sources")
        st.markdown("""
        Works with any video:
        - Khan Academy
        - TED-Ed
        - freeCodeCamp
        - Any video with transcript
        """)
    
    # Main content area
    if not api_key:
        st.warning("⚠️ Please enter your Google Gemini API key in the sidebar to get started.")
        st.info("**Your API key:** `AIzaSyCLcozr0dFqF0Y4Cb8Cwt0KU_3Wy_dJP74`")
        return
    
    # Instructions
    st.info("""
    ### 📋 How to Get Transcript from YouTube:
    
    1. **Go to the YouTube video** you want to learn from
    2. **Click on "..." (three dots)** below the video
    3. **Click "Show transcript"** in the menu
    4. **Copy all the text** that appears (Ctrl+A, then Ctrl+C)
    5. **Paste it** in the box below
    6. **Click "Process Transcript"** button
    """)
    
    # Transcript input
    st.subheader("📝 Paste Video Transcript Here")
    transcript = st.text_area(
        "Paste the complete transcript:",
        height=300,
        placeholder="Paste your YouTube transcript here...\n\nExample:\n0:00\nHello everyone, welcome to this tutorial\n0:05\nToday we'll learn about...",
        help="Copy the entire transcript from YouTube's 'Show transcript' feature"
    )
    
    # Video info (optional)
    col1, col2 = st.columns(2)
    with col1:
        video_title = st.text_input("Video Title (Optional)", placeholder="e.g., Python Tutorial for Beginners")
    with col2:
        video_url = st.text_input("Video URL (Optional)", placeholder="e.g., https://youtube.com/watch?v=...")
    
    if st.button("🚀 Process Transcript", type="primary"):
        if not transcript or len(transcript.strip()) < 50:
            st.error("Please paste a valid transcript (at least 50 characters)")
            return
        
        # Clean transcript (remove timestamps)
        cleaned_transcript = re.sub(r'\d+:\d+\s*', '', transcript)
        
        # Generate cache key for this transcript
        cache_key = get_cache_key(cleaned_transcript)
        
        st.success(f"✅ Transcript received! ({len(cleaned_transcript.split())} words)")
        
        # Store in session state
        st.session_state.transcript = cleaned_transcript
        st.session_state.video_title = video_title or "Untitled Video"
        st.session_state.video_url = video_url
        st.session_state.cache_key = cache_key

        # Simple server-side debug log (appends short lines)
        try:
            with open('jan_project_debug.log', 'a') as _dbg:
                _dbg.write(f"[{datetime.now().isoformat()}] Process Transcript clicked. cache_key={cache_key}\n")
        except Exception:
            pass

        # Call generation functions and persist results to session_state so they survive reruns
        # Summary
        try:
            summary = generate_summary_cached(cleaned_transcript, api_key, cache_key)
            st.session_state.generated_summary = summary
            log_api_call('summary', success=bool(summary), cached=False)
        except Exception as e:
            st.session_state.generated_summary = None
            log_api_call('summary', success=False, cached=False)
            try:
                with open('jan_project_debug.log', 'a') as _dbg:
                    _dbg.write(f"[{datetime.now().isoformat()}] Summary generation error: {str(e)[:200]}\n")
            except Exception:
                pass

        # Key points
        try:
            key_points = extract_key_points_cached(cleaned_transcript, api_key, cache_key)
            st.session_state.generated_keypoints = key_points
            log_api_call('key_points', success=bool(key_points), cached=False)
        except Exception as e:
            st.session_state.generated_keypoints = None
            log_api_call('key_points', success=False, cached=False)
            try:
                with open('jan_project_debug.log', 'a') as _dbg:
                    _dbg.write(f"[{datetime.now().isoformat()}] Key points error: {str(e)[:200]}\n")
            except Exception:
                pass

        # Quiz
        try:
            quiz_data = generate_quiz_cached(cleaned_transcript, api_key, cache_key)
            st.session_state.generated_quiz = quiz_data
            log_api_call('quiz', success=bool(quiz_data), cached=False)
        except Exception as e:
            st.session_state.generated_quiz = None
            log_api_call('quiz', success=False, cached=False)
            try:
                with open('jan_project_debug.log', 'a') as _dbg:
                    _dbg.write(f"[{datetime.now().isoformat()}] Quiz generation error: {str(e)[:200]}\n")
            except Exception:
                pass
        
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
            if video_title:
                st.markdown(f"**Video:** {video_title}")
            if video_url:
                st.markdown(f"**URL:** {video_url}")
            
            with st.expander("View Full Transcript", expanded=False):
                st.text_area("Transcript", cleaned_transcript, height=400)
            
            # Download transcript
            st.download_button(
                label="📥 Download Transcript",
                data=cleaned_transcript,
                file_name=f"transcript_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
        
        # Tab 2: Summary
        with tab2:
            # Show cached/persisted summary if available
            summary = st.session_state.get('generated_summary')
            if summary:
                st.success("✅ Summary available")
                st.subheader("📝 Video Summary")
                st.markdown(summary)
                st.download_button(
                    label="📥 Download Summary",
                    data=summary,
                    file_name=f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
            else:
                st.info("No summary generated yet. Click 'Process Transcript' to generate.")
        
        # Tab 3: Key Points
        with tab3:
            key_points = st.session_state.get('generated_keypoints')
            if key_points:
                st.success("✅ Key points available")
                st.subheader("🎯 Core Learning Points")
                st.markdown(key_points)
                st.download_button(
                    label="📥 Download Key Points",
                    data=key_points,
                    file_name=f"keypoints_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
            else:
                st.info("No key points generated yet. Click 'Process Transcript' to generate.")
        
        # Tab 4: Quiz
        with tab4:
            quiz_data = st.session_state.get('generated_quiz')
            if quiz_data:
                st.success("✅ Quiz available")
                display_quiz(quiz_data)
                quiz_json = json.dumps(quiz_data, indent=2)
                st.download_button(
                    label="📥 Download Quiz (JSON)",
                    data=quiz_json,
                    file_name=f"quiz_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
            else:
                st.info("No quiz generated yet. Click 'Process Transcript' to generate.")

if __name__ == "__main__":
    main()
