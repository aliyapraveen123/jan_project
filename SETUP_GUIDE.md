# 📋 Complete Setup Guide

## Step-by-Step Installation Instructions

### Step 1: Verify Python Installation

Open a terminal and check Python version:
```bash
python --version
# or
python3 --version
```

You need Python 3.8 or higher. If not installed, download from [python.org](https://www.python.org/downloads/).

### Step 2: Navigate to Project Directory

```bash
cd ~/Desktop/"jan project"
```

### Step 3: Create Virtual Environment (Recommended)

**On Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

### Step 4: Install Required Packages

```bash
pip install -r requirements.txt
```

Wait for all packages to install. This may take a few minutes.

### Step 5: Get Google Gemini API Key

1. Open your browser and go to: https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key" button
4. Copy the generated API key
5. Keep it safe - you'll need it when running the app

### Step 6: Run the Application

```bash
streamlit run app.py
```

The app will automatically open in your default browser at `http://localhost:8501`.

### Step 7: Use the Application

1. **Enter API Key**: Paste your Gemini API key in the sidebar
2. **Find a YouTube Video**: Choose any educational video with captions
3. **Copy URL**: Copy the video URL from your browser
4. **Process**: Paste URL in the app and click "Process Video"
5. **Explore**: Navigate through the tabs to see all features

## 🎥 Testing the App

Try these example videos (they have captions):
- Khan Academy videos
- TED-Ed educational content
- Programming tutorials from popular channels
- University lectures

## 🐛 Common Issues and Solutions

### Issue 1: "streamlit: command not found"

**Solution:**
```bash
pip install streamlit --upgrade
# or
python -m streamlit run app.py
```

### Issue 2: "No module named 'youtube_transcript_api'"

**Solution:**
```bash
pip install youtube-transcript-api
```

### Issue 3: "Could not fetch transcript"

**Cause:** Video doesn't have captions enabled

**Solution:** Try a different video that has captions/subtitles

### Issue 4: API Key Error

**Solution:**
- Ensure you copied the complete API key
- Check for extra spaces
- Generate a new key if needed

### Issue 5: Port Already in Use

**Solution:**
```bash
streamlit run app.py --server.port 8502
```

## 🔧 Advanced Configuration

### Change Default Port

```bash
streamlit run app.py --server.port 8080
```

### Run in Headless Mode (No Browser)

```bash
streamlit run app.py --server.headless true
```

### Enable File Watcher

```bash
streamlit run app.py --server.fileWatcherType auto
```

## 📦 Package Details

### Required Packages:

1. **streamlit** (1.31.0)
   - Web application framework
   - Creates interactive UI

2. **youtube-transcript-api** (0.6.2)
   - Fetches video transcripts
   - Handles multiple caption languages

3. **google-generativeai** (0.3.2)
   - Google Gemini AI integration
   - Generates summaries and quizzes

## 🔄 Updating the Application

To update dependencies:
```bash
pip install -r requirements.txt --upgrade
```

## 🛑 Stopping the Application

Press `Ctrl + C` in the terminal where the app is running.

## 📱 Accessing from Other Devices

If you want to access the app from other devices on your network:

```bash
streamlit run app.py --server.address 0.0.0.0
```

Then access via: `http://YOUR_IP_ADDRESS:8501`

## 💾 Saving API Key (Optional)

Create a `.streamlit/secrets.toml` file:

```bash
mkdir -p .streamlit
nano .streamlit/secrets.toml
```

Add:
```toml
GEMINI_API_KEY = "your-api-key-here"
```

Then modify the app to read from secrets (more secure).

## 🎓 Next Steps

After successful setup:
1. Process your first video
2. Explore all tabs (Transcript, Summary, Key Points, Quiz)
3. Take a quiz and check your score
4. Download content for offline study
5. Share with classmates!

## 📞 Getting Help

If you encounter issues:
1. Check the error message in the app
2. Review this setup guide
3. Verify all requirements are installed
4. Check Python and package versions
5. Try with a different YouTube video

## ✅ Verification Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] All packages installed successfully
- [ ] Gemini API key obtained
- [ ] App runs without errors
- [ ] Can access at localhost:8501
- [ ] Successfully processed a test video
- [ ] All tabs work correctly
- [ ] Quiz generates 10 questions
- [ ] Can download content

**Congratulations! Your YouTube Learning Assistant is ready to use! 🎉**
