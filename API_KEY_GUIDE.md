# 🔑 Google Gemini API Key - Complete Guide

## Step-by-Step Instructions with Screenshots Guide

---

## Getting Your Free Google Gemini API Key

### Step 1: Visit Google AI Studio
**URL:** https://makersuite.google.com/app/apikey

OR

**Alternative URL:** https://aistudio.google.com/app/apikey

---

### Step 2: Sign In
- Use your Google account (Gmail)
- If you don't have one, create a free Google account first

---

### Step 3: Create API Key

When you click **"Create API Key"**, it will ask you to:

#### **Name Your Key** ✨
This is just a label for you to identify the key later.

**Suggested Names:**
- `youtube-learning-assistant`
- `youtube-app-key`
- `learning-app`
- `my-youtube-tool`
- `study-helper`
- Or any name you prefer!

**Important:** The name doesn't affect functionality - it's just for your reference.

---

### Step 4: Choose Project (If Asked)

You might see:
- **"Create API key in new project"** ✅ - **CHOOSE THIS** (Recommended!)
- **"Create API key in existing project"** - Only if you have a Google Cloud project
- **"Choose an imported project"** - List of your Google Cloud projects

---

## 🎯 WHAT TO DO:

### Option 1: First Time User (RECOMMENDED)
**Select:** "Create API key in **new project**"

This will automatically create a new Google Cloud project for you.
- Project name: Usually "Generative Language Client" (auto-generated)
- No setup needed
- **EASIEST OPTION**

### Option 2: You See a List of Projects
If you see a dropdown with project names, you can:
- **Choose any existing project** from the list
- **OR click "Create new project"** button

**Tip:** If you're not sure, just select the first project in the list or create a new one.

---

## 📋 Visual Guide:

```
┌──────────────────────────────────────────┐
│ Create API Key                           │
│                                          │
│ Choose where to create the API key:     │
│                                          │
│ ○ Create API key in new project    ✅   │ ← SELECT THIS
│                                          │
│ ○ Create API key in existing project    │
│   ┌────────────────────────────────┐    │
│   │ Select project ▼               │    │
│   └────────────────────────────────┘    │
│                                          │
│              [Continue]                  │
└──────────────────────────────────────────┘
```

It will automatically create a project for you (usually named something like "Generative Language Client").

---

### Step 5: Copy Your API Key

After creating, you'll see:
```
Your API Key: AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

**Important Steps:**
1. ✅ Click the **COPY** button
2. ✅ Save it somewhere safe (notepad, password manager)
3. ✅ Don't share it publicly

---

## Using Your API Key in the App

### Method 1: Paste in Sidebar (Recommended)
1. Run the app: `streamlit run app.py`
2. Look at the **left sidebar**
3. Find the input box labeled **"Enter Google Gemini API Key"**
4. Paste your key
5. Start using the app!

**Note:** The key is only stored in your current session (not saved permanently)

---

### Method 2: Store in Secrets File (Advanced)

If you want to avoid pasting the key every time:

1. **Create secrets directory:**
   ```bash
   mkdir -p ~/.streamlit
   ```

2. **Create secrets file:**
   ```bash
   nano ~/.streamlit/secrets.toml
   ```

3. **Add your key:**
   ```toml
   GEMINI_API_KEY = "YOUR_API_KEY_HERE"
   ```

4. **Save and exit:**
   - Press `Ctrl + X`
   - Press `Y`
   - Press `Enter`

5. **The app will automatically use this key**

---

## Troubleshooting

### Issue 1: "Invalid API Key"

**Possible Causes:**
- ❌ Extra spaces when copying
- ❌ Didn't copy the full key
- ❌ Key was regenerated/deleted

**Solutions:**
1. Copy the key again carefully
2. Make sure you copy the ENTIRE key
3. Paste it directly without typing
4. Generate a new key if needed

---

### Issue 2: "API Key Not Found"

**Solution:**
- Make sure you pasted the key in the sidebar input box
- Check that the key starts with `AIza`

---

### Issue 3: "Quota Exceeded"

**Cause:** You've used the free tier limit

**Solutions:**
1. Wait for the quota to reset (usually next day)
2. Create a new API key
3. Enable billing for higher limits (optional)

---

### Issue 4: Can't Find Where to Enter Key

**Location:** 
- Look at the **LEFT SIDEBAR** of the app
- Scroll down if needed
- You'll see a text input box
- It says "Enter Google Gemini API Key"

---

## API Key Format

A valid Google Gemini API key looks like:
```
AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

**Key Characteristics:**
- Starts with: `AIza`
- Length: ~39 characters
- Contains: Letters, numbers, underscores, hyphens

---

## Free Tier Limits

Google Gemini API Free Tier includes:
- ✅ 60 requests per minute
- ✅ 1,500 requests per day
- ✅ Free forever (no credit card needed)

**What this means for you:**
- You can process **hundreds of videos per day** for FREE
- More than enough for personal/student use

---

## Security Tips

### ✅ DO:
- Keep your API key private
- Don't share it publicly
- Don't commit it to GitHub
- Store it securely

### ❌ DON'T:
- Share your key on social media
- Post it in public forums
- Include it in code you share
- Leave it in screenshots

---

## Quick Reference

### URLs:
- **Get API Key:** https://aistudio.google.com/app/apikey
- **API Documentation:** https://ai.google.dev/

### Key Format:
```
AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

### Where to Paste:
- Open app at http://localhost:8501
- Find sidebar on the LEFT
- Paste in "Enter Google Gemini API Key" box

---

## Complete Walkthrough

### 1. Get the Key:
```
Visit: https://aistudio.google.com/app/apikey
↓
Sign in with Google
↓
Click "Create API Key"
↓
Name it (e.g., "youtube-learning-assistant")
↓
Choose "Create API key in new project"
↓
Copy the key that appears
```

### 2. Use in App:
```
Run: streamlit run app.py
↓
Browser opens at http://localhost:8501
↓
Look at LEFT SIDEBAR
↓
Find input box for API key
↓
Paste your key
↓
Done! Start using the app
```

---

## FAQ

**Q: Do I need a credit card?**
A: No! The free tier requires no payment.

**Q: Will I be charged?**
A: No, unless you manually enable billing.

**Q: Can I use the same key on multiple devices?**
A: Yes, but be mindful of rate limits.

**Q: What if I lose my key?**
A: Just create a new one from the same website.

**Q: Can I have multiple keys?**
A: Yes, you can create multiple API keys.

**Q: Does the key expire?**
A: No, API keys don't expire unless you delete them.

---

## Summary

1. **Visit:** https://aistudio.google.com/app/apikey
2. **Sign in** with Google
3. **Create API Key**
4. **Name it:** (e.g., "youtube-learning-assistant")
5. **Copy** the key
6. **Paste** in the app sidebar
7. **Start learning!** 🚀

---

## Need More Help?

If you're still having trouble:

1. Check that you're on the correct website:
   - ✅ https://aistudio.google.com/app/apikey
   - ✅ https://makersuite.google.com/app/apikey

2. Make sure you're signed in to Google

3. Try a different browser if the page doesn't load

4. Clear your browser cache and try again

---

**You're almost there! Just name your key anything you like (e.g., "youtube-app") and copy it!** 🎉

---

*The key name is just a label for you - it doesn't affect how the app works.*
