# 🎥 Gemini AI Transcript Extraction Guide

## Overview

This project now supports **two methods** for extracting transcripts from YouTube videos:

### 1. 🤖 Gemini AI Extraction (NEW - Recommended)
- Uses Google's Gemini 1.5 Flash model to analyze videos directly
- **Works with videos that don't have captions**
- Can process the video content and generate accurate transcripts
- Requires a valid Gemini API key

### 2. 📝 Traditional Caption API
- Extracts existing closed captions from YouTube
- Fast and efficient for videos with captions
- Falls back automatically if Gemini fails
- No additional API costs

## How It Works

### Gemini AI Method

1. **Video Processing**: When you provide a YouTube URL, the system passes it directly to Gemini AI
2. **AI Analysis**: Gemini watches/analyzes the video content and audio
3. **Transcript Generation**: Gemini generates a comprehensive transcript of all spoken content
4. **Fallback**: If Gemini fails, the system automatically tries the Caption API

### Benefits of Gemini Method

✅ **No Caption Requirement**: Works even if video doesn't have CC
✅ **High Accuracy**: Gemini's advanced AI understands context and nuance
✅ **Multiple Languages**: Can handle various languages and accents
✅ **Complete Coverage**: Captures all spoken content, not just captions

## Usage

### In the Web App

1. Start the application: `streamlit run app.py`
2. Enter your Gemini API key in the sidebar
3. **Check the box**: "Use Gemini AI for transcript extraction" (enabled by default)
4. Paste any YouTube URL
5. Click "Process Video"

### Using the Test Script

```bash
python test_gemini_transcript.py
```

Follow the prompts to:
- Enter your API key
- Provide a YouTube URL
- See the transcript extraction in action

## Technical Details

### Updated Files

1. **`backend/services/transcript_service.py`**
   - Added `use_gemini` parameter to constructor
   - New `get_transcript_with_gemini()` method
   - Enhanced `get_transcript()` with fallback logic

2. **`backend/services/ai_service.py`**
   - Updated to use `gemini-1.5-flash-latest` model
   - Better support for video understanding

3. **`frontend/ui.py`**
   - Added UI toggle for transcript method selection
   - Enhanced error messages and user guidance
   - Passes full YouTube URL to transcript service

### API Models Used

- **Transcript Extraction**: `gemini-1.5-flash-latest`
- **Content Analysis**: `gemini-1.5-flash-latest`

The 1.5 Flash model supports:
- Direct YouTube URL processing
- Video content understanding
- Audio transcription
- Multimodal analysis

## Configuration

### Enable Gemini Transcript Extraction

In the sidebar, check:
```
☑️ Use Gemini AI for transcript extraction
```

### Disable (Use Caption API Only)

Uncheck the box to use traditional captions:
```
☐ Use Gemini AI for transcript extraction
```

## Troubleshooting

### "Gemini returned empty transcript"

**Possible causes:**
- Video is private or restricted
- API quota exceeded
- Network connectivity issues

**Solutions:**
- Check if video is publicly accessible
- Verify API key has quota remaining
- The system will automatically try Caption API fallback

### "Could not fetch transcript using the selected method"

**If using Gemini:**
- Verify API key is valid
- Check API quota at [Google AI Studio](https://makersuite.google.com/app/apikey)
- Try toggling to Caption API method

**If using Caption API:**
- Video must have closed captions (CC button)
- Try toggling to Gemini AI method

## Example Code

### Using Transcript Service Programmatically

```python
from backend.services.transcript_service import TranscriptService
from backend.utils.url_utils import URLUtils

# Setup
api_key = "your-gemini-api-key"
youtube_url = "https://www.youtube.com/watch?v=VIDEO_ID"
video_id = URLUtils.extract_video_id(youtube_url)

# Method 1: Using Gemini AI
service = TranscriptService(api_key=api_key, use_gemini=True)
transcript, _ = service.get_transcript(video_id, youtube_url=youtube_url)

# Method 2: Using Caption API only
service = TranscriptService(use_gemini=False)
transcript, _ = service.get_transcript(video_id)

# Method 3: Auto fallback (Gemini -> Caption API)
service = TranscriptService(api_key=api_key, use_gemini=True)
transcript, _ = service.get_transcript(video_id, youtube_url=youtube_url)
# This will try Gemini first, then Caption API if it fails
```

## Best Practices

1. **Start with Gemini**: Enable Gemini by default for maximum compatibility
2. **Check Results**: Review the first 100-200 words to verify quality
3. **Use Caption API**: For very long videos, Caption API might be faster
4. **Monitor Quota**: Keep track of your Gemini API usage
5. **Save Transcripts**: Download transcripts for offline reference

## API Costs

### Gemini API
- Free tier available with quotas
- Check current pricing at [Google AI Pricing](https://ai.google.dev/pricing)
- Video processing may count toward API limits

### Caption API
- Completely free (uses public YouTube data)
- No API key required for this method
- Limited to videos with existing captions

## Comparison

| Feature | Gemini AI | Caption API |
|---------|-----------|-------------|
| Requires Captions | ❌ No | ✅ Yes |
| API Key Required | ✅ Yes | ❌ No |
| Cost | Small API cost | Free |
| Speed | Slower (video processing) | Faster |
| Accuracy | Very High | Depends on captions |
| Video Length | Any length | Any length |
| Language Support | Excellent | Based on captions |

## Recommendations

### Use Gemini When:
- Video doesn't have captions
- You need the highest accuracy
- Video has poor quality captions
- Video has multiple speakers

### Use Caption API When:
- Video has good quality captions
- You want fastest processing
- You want to minimize API costs
- Processing many videos in batch

## Future Enhancements

Potential improvements:
- Timestamp preservation with Gemini transcripts
- Multi-language transcript generation
- Speaker identification
- Automatic quality scoring
- Batch processing optimization

---

For questions or issues, please refer to the main README.md or create an issue in the repository.
