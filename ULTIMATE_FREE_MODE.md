# 🚀 ULTIMATE FREE MODE - Setup Guide

## What You Get

### ✅ 4 Powerful Free Features:

1. **Multi-Key Rotation** (3x quota = 60 requests/day)
2. **Smart Caching** (saves ~4 API calls per repeated video)
3. **Caption-First Strategy** (saves 1 API call per video with captions)
4. **Rate Limiting** (prevents 429 errors)

---

## Quick Setup (5 minutes)

### Step 1: Get 2 More Free API Keys

Visit: https://aistudio.google.com/app/apikey

**Create 2 more free Google accounts** and get API keys for each:
- Use different emails (Gmail, Outlook, etc.)
- Each account gets 20 requests/day
- Total: **60 requests/day** (3 accounts × 20)

### Step 2: Add Keys to .env File

Open `.env` file and add your keys:

```bash
GOOGLE_API_KEY=AIzaSyCDGL6wuNMsBOnxAEnjM8yDNCRj0bumAwM
GOOGLE_API_KEY_2=your_second_api_key_here
GOOGLE_API_KEY_3=your_third_api_key_here
```

**Note:** Keys 2 and 3 are optional. The app works with 1 key, but more keys = more quota!

### Step 3: Run the App

```bash
streamlit run app.py
```

That's it! 🎉

---

## How It Works

### 🔄 Multi-Key Rotation

The app automatically:
- Rotates between all available API keys
- Tracks usage for each key (20 requests/day limit)
- Switches to next key when one is exhausted
- Resets counters daily

**Example:**
- Key 1: Process 20 videos
- Key 2: Process 20 more videos
- Key 3: Process 20 more videos
- **Total: 60 videos/day!**

### 💾 Smart Caching

Once a video is processed, it's cached locally:
- **First time**: Uses 3-4 API calls
- **Next time**: Uses 0 API calls (instant!)

Cache is stored in `cache/` folder:
```
cache/
  transcripts/
  summaries/
  keypoints/
  quizzes/
  api_usage.json
```

**Benefits:**
- Instant results for repeated videos
- No API calls wasted
- Works even if quota exhausted

### 📹 Caption-First Strategy

The app tries to get transcripts in this order:
1. **YouTube captions** (0 API calls) ✅ FREE
2. **Audio download + AI transcription** (1 API call) 💰 COSTS QUOTA

**Pro Tip:** Choose videos with captions enabled:
- Khan Academy
- TED Talks
- Coursera
- YouTube EDU channels

### ⏱️ Smart Rate Limiting

Prevents 429 errors by:
- Waiting 13 seconds between API calls
- Respecting 5 requests/minute limit
- Automatic retry with exponential backoff

---

## Daily Capacity Calculator

### With 1 API Key (20 requests/day):
- Videos **with captions**: ~6 videos/day (3 API calls each)
- Videos **without captions**: ~5 videos/day (4 API calls each)

### With 3 API Keys (60 requests/day):
- Videos **with captions**: ~20 videos/day 🚀
- Videos **without captions**: ~15 videos/day 🚀
- **Mixed videos**: ~18 videos/day 🚀

### With Caching:
- **Unlimited** repeated videos! 🎉
- Only new videos count toward quota

---

## Usage Stats & Monitoring

The app shows real-time stats:

```
📊 API Keys Status
Key 1: 15/20 requests used
Key 2: 8/20 requests used
Key 3: 3/20 requests used

💾 Cache Status
📦 Cached videos: 12
✅ Cache saves: ~48 API calls saved!
```

---

## Pro Tips

### 1. Maximize Your Quota:
- Use videos with captions (saves 1 API call)
- Re-watch cached videos (saves 3-4 API calls)
- Process videos during off-peak hours

### 2. Get More Keys:
- Create Google accounts with different emails
- Use family members' accounts (with permission)
- Each account = +20 requests/day

### 3. Cache Management:
- Cache persists between app restarts
- Located in `cache/` folder
- Delete `cache/` folder to clear all cache
- Delete specific video: `cache/transcripts/VIDEO_ID.json`

### 4. Best Videos to Process:
- ✅ Khan Academy (always has captions)
- ✅ TED Talks (always has captions)
- ✅ Coursera lectures (usually has captions)
- ✅ YouTube EDU channels
- ❌ Avoid: Short clips, music videos, private videos

---

## Troubleshooting

### "All API keys exhausted for today"
**Solution:** Wait until midnight (resets daily) or add more API keys

### "Could not extract transcript"
**Possible reasons:**
1. Video is private/age-restricted
2. No captions available + audio extraction failed
3. API quota exhausted

**Solution:** Try a different video with captions enabled

### "429 Error: Rate limit exceeded"
**Solution:** This shouldn't happen with the 13-second delays. If it does:
1. Increase delay in `ui.py`: `time.sleep(15)` instead of 13
2. Restart the app

### Cache not working
**Check:**
1. `cache/` folder exists in project root
2. Write permissions are enabled
3. No disk space issues

---

## File Structure

```
jan project/
├── app.py
├── .env                          # API keys here
├── cache/                        # Auto-created
│   ├── transcripts/
│   ├── summaries/
│   ├── keypoints/
│   ├── quizzes/
│   └── api_usage.json           # Usage tracking
├── backend/
│   ├── services/
│   │   ├── ai_service.py        # AI generation with key rotation
│   │   └── transcript_service.py # Caption-first extraction
│   └── utils/
│       ├── cache_manager.py     # NEW: Cache system
│       └── api_key_rotator.py   # NEW: Key rotation
└── frontend/
    └── ui.py                     # Updated with all features
```

---

## Cost Comparison

### Free Tier (This Setup):
- **Cost**: $0/month 💰
- **Capacity**: 60 requests/day (3 keys)
- **Videos**: ~15-20 videos/day
- **Caching**: Unlimited repeated videos

### Paid Tier (Google AI):
- **Cost**: ~$5-10/month 💸
- **Capacity**: Unlimited requests*
- **Videos**: Unlimited
- **Benefit**: No delays, no key rotation

**This free setup is perfect for:**
- Students learning 15-20 videos/day
- Teachers creating study materials
- Personal learning projects
- Testing before upgrading

---

## What's Next?

### Already Implemented ✅:
- ✅ Multi-key rotation
- ✅ Smart caching
- ✅ Caption-first strategy
- ✅ Rate limiting
- ✅ Usage tracking
- ✅ Real-time stats

### Future Improvements (Optional):
- [ ] Export cache as JSON/CSV
- [ ] Batch processing queue
- [ ] Email notifications for quota resets
- [ ] Cloud backup for cache
- [ ] Browser extension for one-click processing

---

## Support

**Having issues?**
1. Check `.env` file has valid API keys
2. Verify internet connection
3. Try a different video (with captions)
4. Check `cache/api_usage.json` for quota status
5. Restart the app: `streamlit run app.py`

**Want to contribute?**
- Add more optimization features
- Improve caching logic
- Create better UI/UX
- Add analytics dashboard

---

## Summary

🎉 **You now have an ULTIMATE FREE YouTube Learning Assistant that:**
- Processes 15-20 videos/day (60 requests)
- Caches results for instant re-access
- Prioritizes free captions over expensive transcription
- Never hits rate limits
- Tracks usage across multiple keys
- Costs $0/month

**Enjoy learning! 🚀📚**
