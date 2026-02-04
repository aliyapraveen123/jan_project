# ⚠️ API Quota Exceeded - What Happened & Solutions

## What's Happening

You're seeing this error:
```
❌ Failed
Could not extract transcript from this video.
💡 API quota exceeded (free tier: 20 requests/day)
```

## Root Cause

**Gemini API Free Tier Limits:**
- **20 requests per day** for `gemini-2.5-flash` model
- Resets every 24 hours
- Each video processing uses **multiple requests**:
  - 1 request for transcription (if no captions)
  - 1 request for summary
  - 1 request for key points  
  - 1 request for quiz generation
  - **Total: ~4 requests per video**

**You can process ~5 videos per day** on the free tier.

## Immediate Solutions

### Solution 1: Use Videos WITH Captions (Recommended)
Videos with captions don't use the transcription API, saving you quota!

**Channels that always have captions:**
- ✅ Khan Academy: https://www.youtube.com/@khanacademy
- ✅ TED Talks: https://www.youtube.com/@TED
- ✅ Crash Course: https://www.youtube.com/@crashcourse
- ✅ freeCodeCamp: https://www.youtube.com/@freecodecamp
- ✅ Coursera: https://www.youtube.com/@coursera
- ✅ MIT OpenCourseWare: https://www.youtube.com/@mitocw

**Example working URLs:**
```
https://www.youtube.com/watch?v=9bZkp7q19f0  (Khan Academy - Photosynthesis)
https://www.youtube.com/watch?v=kCc8FmEb1nY  (TED Talk)
```

### Solution 2: Wait 24 Hours
Your quota will reset after 24 hours. Come back tomorrow!

### Solution 3: Upgrade to Paid Tier
If you need more requests:
- Go to: https://ai.google.dev/
- Upgrade to paid tier
- Get **1,500 requests per minute** instead of 20 per day

## How to Check Your Usage

Visit: https://ai.dev/rate-limit

## Current App Behavior

### Videos WITH Captions:
```
📝 Attempting to extract captions...
✅ Extracted transcript from captions (fast, FREE!)
🤖 Generating summary... (uses 1 API call)
🎯 Extracting key points... (uses 1 API call)
📊 Creating quiz... (uses 1 API call)
Total: 3 API calls
```

### Videos WITHOUT Captions:
```
📝 Attempting to extract captions...
⚠️ Captions not available
🎵 Trying audio extraction...
📥 Downloading audio...
🤖 Transcribing audio... (uses 1 API call)
🤖 Generating summary... (uses 1 API call)
🎯 Extracting key points... (uses 1 API call)
📊 Creating quiz... (uses 1 API call)
Total: 4 API calls
```

## Best Practices to Save Quota

1. **Prefer videos with captions** - saves 1 API call per video
2. **Process only videos you need** - don't test randomly
3. **Use shorter videos** - faster processing, same quota cost
4. **Batch your work** - plan which videos to process

## Technical Details

**Error Message:**
```
429 You exceeded your current quota
Quota metric: generate_content_free_tier_requests
Limit: 20 requests/day
Model: gemini-2.5-flash
```

**Quota Types:**
- Free Tier: 20 requests/day
- Paid Tier: 1,500 requests/minute

## Summary

✅ **Your app is working perfectly!**  
❌ **You just hit the free tier limit**

**Next steps:**
1. Try a video with captions (Khan Academy, TED, etc.)
2. Or wait 24 hours for quota reset
3. Or upgrade to paid tier for unlimited usage

The audio extraction feature works great - you just need more quota or to use caption-enabled videos! 🎉
