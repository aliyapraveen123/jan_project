# 🎯 Quick Start Guide

## 5-Minute Setup

### 1. Get Your API Key (2 minutes)
1. Go to: https://makersuite.google.com/app/apikey
2. Sign in with Google
3. Click "Create API Key"
4. Copy the key

### 2. Run the App (1 minute)
```bash
cd ~/Desktop/"jan project"
./run.sh
```

Or manually:
```bash
cd ~/Desktop/"jan project"
source .venv/bin/activate
streamlit run app.py
```

### 3. Use the App (2 minutes)
1. Paste your API key in the sidebar
2. Copy any YouTube video URL (with captions)
3. Click "Process Video"
4. Explore the 4 tabs!

## 🎬 Try These Videos

**Sample URLs with captions:**
- Khan Academy: Search "Khan Academy" + any topic
- TED-Ed: Search "TED-Ed" + any topic
- Programming: "Python tutorial for beginners"
- Science: "How does DNA work"

## ✨ Features Summary

| Feature | What It Does | Output |
|---------|-------------|---------|
| **Transcript** | Extracts full video text | Downloadable .txt file |
| **Summary** | AI-generated overview | Structured markdown |
| **Key Points** | 8-12 critical facts | Numbered list |
| **Quiz** | 10 MCQ questions | Interactive test |

## 🔧 Troubleshooting Quick Fix

**Problem:** Can't fetch transcript
**Solution:** Video needs captions - try a different video

**Problem:** API error
**Solution:** Check your API key, regenerate if needed

**Problem:** Port in use
**Solution:** Run `streamlit run app.py --server.port 8502`

## 📱 Access from Phone

1. Find your computer's IP: `hostname -I`
2. Run: `streamlit run app.py --server.address 0.0.0.0`
3. Open: `http://YOUR_IP:8501` on phone

## 💡 Pro Tips

- **Long videos work best** - More content = Better quizzes
- **Educational content** - Works best with structured learning material
- **Download everything** - Save summaries for offline study
- **Retry quiz** - Learn from explanations and try again

## 🎓 Perfect For

- **Before exams** - Quick revision from lecture videos
- **Self-learning** - Extract notes from tutorials
- **Homework help** - Understand difficult topics
- **Test prep** - Practice with auto-generated quizzes

---

**Ready? Let's go! 🚀**

```bash
streamlit run app.py
```
