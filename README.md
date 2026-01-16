# 🎓 YouTube Learning Assistant

An advanced AI-driven system that transforms YouTube educational videos into structured learning content with summaries, key points, and interactive quizzes.

## ✨ Features

### 1. **Automatic Transcript Extraction**
- Extracts full transcripts from any YouTube video with captions
- Supports all YouTube URL formats
- Handles videos of any length
- Download transcript as text file

### 2. **AI-Generated Summaries**
- Comprehensive video summaries using Google Gemini AI
- Organized into clear sections
- Brief overview and detailed breakdown
- Main topics and key takeaways
- Download summary for offline study

### 3. **Core Learning Points**
- Automatically identifies 8-12 critical learning points
- Exam-oriented content extraction
- Clear and concise format
- Easy to review and memorize
- Download for revision notes

### 4. **Interactive Quiz Generation**
- Generates exactly 10 multiple-choice questions from video content
- Questions based on actual transcript, not generic content
- 4 options per question (A, B, C, D)
- Instant feedback on answers
- Detailed explanations for each question
- Score tracking and performance feedback
- Download quiz as JSON file

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key (free from [Google AI Studio](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone or download this project**
   ```bash
   cd "jan project"
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Linux/Mac
   # or
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Get Your API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key (keep it secure!)

## 📖 How to Use

1. **Start the application**
   ```bash
   streamlit run app.py
   ```

2. **Open in browser**
   - The app will automatically open at `http://localhost:8501`

3. **Configure API Key**
   - Enter your Google Gemini API key in the sidebar

4. **Process a Video**
   - Paste any YouTube video URL
   - Click "Process Video"
   - Wait for AI to analyze the content

5. **Explore the Content**
   - **Transcript Tab**: View and download the full transcript
   - **Summary Tab**: Read AI-generated comprehensive summary
   - **Key Points Tab**: Study the most important learning points
   - **Quiz Tab**: Test your understanding with 10 questions

6. **Take the Quiz**
   - Answer all 10 questions
   - Click "Submit Quiz" to see results
   - Review explanations for missed questions
   - Click "Reset Quiz" to try again

## 🎯 Use Cases

### For Students
- Quick revision before exams
- Extract notes from lecture videos
- Self-assessment through quizzes
- Understand complex topics faster

### For Educators
- Create study materials from videos
- Generate quiz questions automatically
- Identify key concepts to teach
- Supplement course content

### For Self-Learners
- Learn from any YouTube tutorial
- Track understanding through quizzes
- Save time on note-taking
- Focus on important points

## 🔧 Technical Details

### Technologies Used
- **Streamlit**: Web interface
- **YouTube Transcript API**: Extract video transcripts
- **Google Gemini AI**: Generate summaries, key points, and quizzes
- **Python**: Backend processing

### Key Components

1. **Transcript Extraction**
   - Uses `youtube-transcript-api` library
   - Supports multiple caption languages
   - Handles various YouTube URL formats

2. **AI Processing**
   - Google Gemini Pro model
   - Custom prompts for each feature
   - Structured output formatting

3. **Quiz Generation**
   - Ensures exactly 10 questions
   - JSON-based structure
   - Validation and error handling

## 📝 Features in Detail

### Summary Generation
The AI analyzes the entire transcript and provides:
- Brief overview (2-3 sentences)
- Main topics covered (bullet points)
- Detailed summary by sections
- Key takeaways for quick reference

### Key Points Extraction
Identifies the most critical information:
- 8-12 essential learning points
- Factual and specific content
- Exam-oriented focus
- Clear explanations

### Quiz Features
- Exactly 10 multiple-choice questions
- Mixed difficulty levels (easy, medium, hard)
- Instant feedback on submission
- Detailed explanations for learning
- Score tracking with percentage
- Performance-based feedback

## 🔒 Privacy & Security

- API key stored only in session (not saved)
- No video content stored permanently
- All processing done in real-time
- No user data collection

## ⚠️ Troubleshooting

### "Could not fetch transcript"
- Ensure the video has captions/subtitles enabled
- Try videos with auto-generated captions
- Check if the video is publicly accessible

### "Error configuring API"
- Verify your API key is correct
- Check if you have API quota remaining
- Ensure you copied the entire key

### Quiz Generation Issues
- If less than 10 questions generated, the system auto-retries
- Longer videos work better for quiz generation
- Ensure video has substantial educational content

## 📚 Example Videos to Try

Try these types of educational videos:
- Programming tutorials
- Science lectures
- Math explanations
- History documentaries
- Language lessons
- Business courses

## 🤝 Contributing

Feel free to enhance this project by:
- Adding support for more languages
- Implementing flashcard generation
- Adding export to PDF
- Supporting video playlists
- Adding more quiz question types

## 📄 License

This project is open-source and free to use for educational purposes.

## 🙏 Acknowledgments

- Google Gemini AI for powerful language models
- YouTube Transcript API for transcript extraction
- Streamlit for the beautiful web interface

---

**Made with ❤️ for students and learners everywhere**

For issues or questions, please refer to the documentation or check the error messages in the app.
