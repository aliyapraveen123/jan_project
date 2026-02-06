# 🚀 Quick Setup Guide - .env Configuration

## Why Use .env File?

✅ **Better User Experience**: No need to enter API key every time  
✅ **More Secure**: API key not exposed in UI  
✅ **Easier Setup**: Configure once, use forever  
✅ **Professional**: Industry-standard approach  

## Setup in 3 Steps

### Step 1: Get Your API Key
Visit: https://aistudio.google.com/app/apikey
- Sign in with Google
- Click "Create API Key"
- Copy the key

### Step 2: Configure .env File

**Option A: Already have .env file**
```bash
# Just edit the .env file
nano .env

# Or open in any text editor and update:
GOOGLE_API_KEY=your_actual_api_key_here
```

**Option B: Create new .env file**
```bash
# Copy the example file
cp .env.example .env

# Edit it
nano .env

# Replace "your_api_key_here" with your actual key:
GOOGLE_API_KEY=AIzaSyA0wk9hLDX8uNxW8ySZtj13f3LeiTn4CkM
```

### Step 3: Run the App
```bash
streamlit run app.py
```

That's it! The app will automatically load your API key. 🎉

## What You'll See

### With .env Configured ✅
```
⚙️ Configuration
✅ API Key loaded from .env file
```
- No need to enter key manually
- Start using immediately
- Optional override available in expander

### Without .env ⚠️
```
⚙️ Configuration
⚠️ No API key found in .env file
Enter Google Gemini API Key: [           ]
```
- Must enter key manually each time
- Key not saved between sessions

## Verification

Check if your .env is working:

```bash
# View your .env file (in terminal)
cat .env

# Should show:
# GOOGLE_API_KEY=AIzaSyA0wk9hLDX8uNxW8ySZtj13f3LeiTn4CkM
```

## Troubleshooting

### "No API key found in .env file"

**Check 1: File exists**
```bash
ls -la .env
# Should show the file
```

**Check 2: File has correct content**
```bash
cat .env
# Should show: GOOGLE_API_KEY=your_key
```

**Check 3: No spaces around =**
```bash
# ✅ Correct
GOOGLE_API_KEY=AIzaSyA...

# ❌ Wrong (spaces)
GOOGLE_API_KEY = AIzaSyA...
```

**Check 4: Restart the app**
```bash
# Stop with Ctrl+C
# Then restart
streamlit run app.py
```

### "API key is invalid"

**Solution:** Get a new key from https://aistudio.google.com/app/apikey

## Security Tips

### ✅ DO:
- Keep `.env` in `.gitignore` (already configured)
- Never commit `.env` to version control
- Keep your API key private
- Use `.env.example` for templates

### ❌ DON'T:
- Share your `.env` file
- Commit API keys to git
- Post API keys online
- Share screenshots with keys visible

## File Structure

```
jan project/
├── .env                  ← Your actual API key (keep private!)
├── .env.example          ← Template file (safe to share)
├── .gitignore            ← Ensures .env is not committed
├── app.py                ← Main application
└── ...
```

## Updating Your API Key

If you need to change your API key:

```bash
# 1. Get new key from Google AI Studio
# 2. Edit .env file
nano .env

# 3. Replace old key with new key
GOOGLE_API_KEY=new_key_here

# 4. Restart app
streamlit run app.py
```

## Advanced: Override API Key

Even with .env configured, you can use a different key:

1. Run the app
2. In sidebar, expand "🔑 Override API Key (Optional)"
3. Enter different key
4. That session will use the new key

Perfect for testing with multiple keys!

## Comparison

| Method | Ease of Use | Security | Setup Time |
|--------|-------------|----------|------------|
| .env file | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 2 minutes |
| Manual entry | ⭐⭐ | ⭐⭐⭐ | Every time |

## Need Help?

1. **Check .env file exists**: `ls -la .env`
2. **Check content**: `cat .env`
3. **Verify format**: No spaces, correct key
4. **Restart app**: Stop (Ctrl+C) and run again
5. **Check API key**: Test at Google AI Studio

---

## Quick Commands Reference

```bash
# Create .env from template
cp .env.example .env

# Edit .env
nano .env

# View .env (verify)
cat .env

# Run app
streamlit run app.py

# Stop app
# Press Ctrl+C
```

---

**Pro Tip**: Once configured, you never have to think about the API key again! Just run `streamlit run app.py` and start learning! 🎓✨
