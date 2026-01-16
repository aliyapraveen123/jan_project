# 📁 Project Structure

## YouTube Learning Assistant - Organized Architecture

This project follows a clean separation between **backend** (business logic) and **frontend** (user interface).

---

## 📂 Directory Structure

```
jan project/
│
├── 📁 backend/                  # Backend Module (Business Logic)
│   ├── __init__.py
│   ├── 📁 services/             # Core Services
│   │   ├── __init__.py
│   │   ├── transcript_service.py    # YouTube transcript extraction
│   │   └── ai_service.py            # AI content generation (Gemini)
│   └── 📁 utils/                # Utility Functions
│       ├── __init__.py
│       ├── url_utils.py             # URL parsing & video ID extraction
│       └── file_utils.py            # File operations & downloads
│
├── 📁 frontend/                 # Frontend Module (User Interface)
│   ├── __init__.py
│   ├── ui.py                        # Main Streamlit UI
│   └── 📁 components/           # UI Components
│       ├── __init__.py
│       └── quiz_component.py        # Interactive quiz display
│
├── 📁 docs/                     # Documentation (existing .md files)
│   ├── README.md
│   ├── SETUP_GUIDE.md
│   ├── QUICKSTART.md
│   ├── FEATURES.md
│   ├── EXAMPLES.md
│   └── ... (other documentation)
│
├── app.py                       # Main Entry Point
├── requirements.txt             # Python Dependencies
├── run.sh                       # Quick Launch Script
├── test_system.py               # System Tests
└── .gitignore                   # Git Ignore Rules
```

---

## 🔧 Module Breakdown

### Backend Module (`backend/`)

#### **Services** (`backend/services/`)

1. **`transcript_service.py`** - YouTube Transcript Extraction
   - `TranscriptService.get_transcript(video_id)` - Fetch video transcript
   - `TranscriptService.get_transcript_info(video_id)` - Get transcript metadata
   - Handles multiple languages and caption types

2. **`ai_service.py`** - AI Content Generation
   - `AIService.generate_summary(transcript)` - Generate video summary
   - `AIService.extract_key_points(transcript)` - Extract learning points
   - `AIService.generate_quiz(transcript)` - Create 10 quiz questions
   - Uses Google Gemini Pro AI model

#### **Utilities** (`backend/utils/`)

1. **`url_utils.py`** - URL Operations
   - `URLUtils.extract_video_id(url)` - Extract video ID from URL
   - `URLUtils.is_valid_youtube_url(url)` - Validate YouTube URL
   - `URLUtils.clean_url(url)` - Remove extra parameters

2. **`file_utils.py`** - File Operations
   - `FileUtils.generate_filename()` - Create timestamped filenames
   - `FileUtils.format_quiz_json()` - Format quiz as JSON
   - `FileUtils.get_file_mime_type()` - Get MIME types

---

### Frontend Module (`frontend/`)

1. **`ui.py`** - Main Streamlit Interface
   - Page configuration
   - API key management
   - Video processing workflow
   - Tab-based content display

2. **Components** (`frontend/components/`)
   - **`quiz_component.py`** - Interactive Quiz
     - `display_quiz(quiz_data)` - Render quiz interface
     - Score tracking
     - Answer feedback
     - Performance evaluation

---

## 🚀 How It Works

### Application Flow:

```
1. User enters API key (sidebar)
   ↓
2. User inputs YouTube URL
   ↓
3. Frontend (ui.py) validates URL
   ↓
4. Backend (transcript_service.py) fetches transcript
   ↓
5. Backend (ai_service.py) processes content:
   - Generate summary
   - Extract key points
   - Create quiz
   ↓
6. Frontend displays results in tabs:
   - Transcript tab
   - Summary tab
   - Key Points tab
   - Quiz tab (using quiz_component.py)
   ↓
7. User can download all content
```

---

## 💻 Running the Application

### Method 1: Using Main Entry Point
```bash
cd ~/Desktop/"jan project"
streamlit run app.py
```

### Method 2: Using Frontend Directly
```bash
cd ~/Desktop/"jan project"
streamlit run frontend/ui.py
```

### Method 3: Using Launch Script
```bash
cd ~/Desktop/"jan project"
./run.sh
```

---

## 🔌 API Reference

### Backend Services

#### TranscriptService
```python
from backend.services.transcript_service import TranscriptService

service = TranscriptService()
transcript, data = service.get_transcript("VIDEO_ID")
```

#### AIService
```python
from backend.services.ai_service import AIService

ai = AIService(api_key="YOUR_API_KEY")
summary = ai.generate_summary(transcript)
key_points = ai.extract_key_points(transcript)
quiz = ai.generate_quiz(transcript)
```

#### URLUtils
```python
from backend.utils.url_utils import URLUtils

video_id = URLUtils.extract_video_id(url)
is_valid = URLUtils.is_valid_youtube_url(url)
```

---

## 📦 Dependencies

All dependencies are in `requirements.txt`:
```
streamlit==1.31.0
youtube-transcript-api==0.6.2
google-generativeai==0.3.2
```

---

## 🧪 Testing

### Test Individual Modules:

```python
# Test Transcript Service
from backend.services.transcript_service import TranscriptService
service = TranscriptService()
transcript, _ = service.get_transcript("kqtD5dpn9C8")
print(f"Transcript length: {len(transcript)}")

# Test URL Utils
from backend.utils.url_utils import URLUtils
video_id = URLUtils.extract_video_id("https://www.youtube.com/watch?v=abc123")
print(f"Video ID: {video_id}")
```

### Run System Tests:
```bash
cd ~/Desktop/"jan project"
python test_system.py
```

---

## 🎯 Benefits of This Structure

### ✅ **Separation of Concerns**
- Backend handles all business logic
- Frontend focuses on UI/UX
- Easy to maintain and update

### ✅ **Modularity**
- Each module has a specific purpose
- Easy to test components individually
- Reusable code

### ✅ **Scalability**
- Easy to add new services
- Can add more UI components
- Can switch frontend framework easily

### ✅ **Maintainability**
- Clear code organization
- Easy to find and fix bugs
- Well-documented structure

---

## 📝 Adding New Features

### Add a New Backend Service:
1. Create file in `backend/services/`
2. Define service class
3. Import in `frontend/ui.py`

### Add a New Frontend Component:
1. Create file in `frontend/components/`
2. Define component function
3. Import in `frontend/ui.py`

### Example - Adding a Flashcard Service:
```python
# backend/services/flashcard_service.py
class FlashcardService:
    def generate_flashcards(self, transcript):
        # Implementation
        pass

# frontend/components/flashcard_component.py
def display_flashcards(flashcards):
    # Render flashcards
    pass
```

---

## 🔄 Migration Notes

The old `app.py` has been renamed to `app_old.py` for reference. The new architecture provides:
- Better code organization
- Easier testing
- Improved maintainability
- Cleaner separation of concerns

All functionality remains the same!

---

## 📚 Documentation

Complete documentation available in `/docs/` folder:
- SETUP_GUIDE.md - Installation instructions
- QUICKSTART.md - 5-minute quick start
- FEATURES.md - Feature specifications
- EXAMPLES.md - Usage examples
- TROUBLESHOOTING.md - Common issues

---

## 🎓 For Developers

### Backend Development:
- All business logic in `backend/`
- Services are self-contained
- Use type hints for clarity
- Add docstrings to all functions

### Frontend Development:
- All UI code in `frontend/`
- Use Streamlit components
- Keep UI logic separate from business logic
- Components should be reusable

---

**The new structure makes the project more professional, maintainable, and scalable! 🚀**
