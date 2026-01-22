# 🚨 API Quota Exceeded - Quick Fix Guide

## Problem:
You've exceeded the free tier daily quota for Google Gemini API.

## Solution 1: Create a New API Key (2 minutes)

### Step 1: Go to Google AI Studio
https://aistudio.google.com/app/apikey

### Step 2: Create New API Key
1. Click "Create API key"
2. Choose "Create API key in new project"
3. Copy the new key

### Step 3: Update Your .env File
```bash
nano .env
```

Replace the old key with your new key:
```
GOOGLE_API_KEY=your_new_api_key_here
```

Save: Ctrl+X → Y → Enter

### Step 4: Restart App
```bash
pkill -f streamlit
./run.sh
```

## Solution 2: Wait for Reset
- Free tier quotas reset every 24 hours
- Wait until tomorrow and try again
- Your cached results will still work instantly!

## Solution 3: Upgrade to Paid Plan
- Get 50x more requests
- $0.00001 per request (very cheap)
- Visit: https://ai.google.dev/pricing

## 💡 Pro Tips to Avoid This:
1. ✅ Use the SAME transcript multiple times (cache = free)
2. ✅ Download your results to save them
3. ✅ Process fewer videos per day on free tier
4. ✅ Create multiple API keys for different projects

## Current Quota Status:
Check your usage at: https://console.cloud.google.com/apis/api/generativelanguage.googleapis.com/quotas
