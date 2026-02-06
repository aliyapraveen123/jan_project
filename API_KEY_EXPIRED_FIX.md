# ⚠️ URGENT: Your API Key Has Expired

## Quick Fix (2 minutes)

### Step 1: Get New API Key

1. Go to: **https://aistudio.google.com/app/apikey**
2. Click **"Create API Key"**
3. Select your Google Cloud project (or create new one)
4. Copy the new key

### Step 2: Update .env File

Open `.env` file and replace the expired key with your new key:

```bash
GOOGLE_API_KEY=your_new_key_here
GOOGLE_API_KEY_2=your_second_api_key_here  # Optional
GOOGLE_API_KEY_3=your_third_api_key_here   # Optional
```

### Step 3: Restart App

```bash
streamlit run app.py
```

---

## 🚀 BONUS: Get 2 More Keys for 3x Capacity!

To get **60 requests/day instead of 20**:

1. Create 2 more free Google accounts (use different emails)
2. Get API keys from each account at: https://aistudio.google.com/app/apikey
3. Add all 3 keys to `.env` file

**Example:**
```bash
GOOGLE_API_KEY=AIzaSyABC...key1
GOOGLE_API_KEY_2=AIzaSyDEF...key2
GOOGLE_API_KEY_3=AIzaSyGHI...key3
```

This gives you:
- **60 API requests/day** (20 per key × 3 keys)
- **15-20 videos/day** processing capacity
- Automatic key rotation when one is exhausted

---

## What's New in ULTIMATE FREE MODE?

✅ **Multi-Key Rotation** - Automatically rotates between 3 API keys
✅ **Smart Caching** - Saves processed videos, instant re-access (0 API calls)
✅ **Caption-First** - Uses YouTube captions first (saves 1 API call per video)
✅ **Rate Limiting** - 13-second delays prevent 429 errors
✅ **Usage Tracking** - Real-time stats for all keys
✅ **Cache Stats** - See how many API calls you've saved

---

## Features at a Glance

### Dashboard Shows:
- API keys usage (15/20 requests used)
- Remaining quota per key
- Total cached videos
- API calls saved by caching

### Smart Processing:
1. **Check cache first** - If video already processed, use cache (instant!)
2. **Try captions** - If video has captions, use them (saves 1 API call)
3. **Rotate keys** - Automatically switches to next available key
4. **Track usage** - Records every API call to prevent overages
5. **Save results** - Caches everything for next time

---

## Ready to Use!

After updating your API key, the app will:
1. Show usage stats for all your keys
2. Process videos super efficiently
3. Cache results for instant re-access
4. Automatically rotate between keys
5. Never hit rate limits

**Check `ULTIMATE_FREE_MODE.md` for complete documentation!**
