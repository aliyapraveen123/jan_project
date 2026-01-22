# API Key Security Guide

## ⚠️ CRITICAL: Never Share Your API Key!

Your API key is like a password. Anyone with your key can use your Google AI quota and potentially incur costs.

## How to Set Up API Key Securely

### Method 1: Environment Variables (Recommended)

1. **Create a `.env` file** in the project root:
   ```bash
   # Copy the example file
   cp .env.example .env
   ```

2. **Edit `.env` and add your API key**:
   ```
   GOOGLE_API_KEY=your_actual_api_key_here
   ```

3. **Install python-dotenv** (if not already installed):
   ```bash
   source .venv/bin/activate
   pip install python-dotenv
   ```

4. **The app will automatically load from `.env`** - the code already supports this!

5. **Verify `.env` is in `.gitignore`** - it should never be committed to GitHub

### Method 2: Streamlit Secrets (Alternative)

1. Create `.streamlit/secrets.toml`:
   ```toml
   GOOGLE_API_KEY = "your_actual_api_key_here"
   ```

2. Access in code:
   ```python
   import streamlit as st
   api_key = st.secrets["GOOGLE_API_KEY"]
   ```

### Method 3: Enter in UI (Current Method)

- Enter your API key in the sidebar when running the app
- ⚠️ **Drawback**: Need to re-enter every time you restart the app
- ✅ **Benefit**: Key never stored in code or files

## What to Do If Your Key Was Exposed

1. **Immediately revoke the key** at https://aistudio.google.com/app/apikey
2. **Generate a new key**
3. **Update your `.env` file** with the new key
4. **Never paste keys in chat or commit them to Git**

## Best Practices

✅ **DO:**
- Use `.env` files for local development
- Add `.env` to `.gitignore`
- Use environment variables in production
- Rotate keys periodically
- Use different keys for dev/prod

❌ **DON'T:**
- Commit API keys to GitHub
- Share keys in chat/email
- Hardcode keys in source code
- Use the same key across multiple projects
- Leave exposed keys active

## Checking Your Security

Run this to verify `.env` won't be committed:
```bash
git status  # Should NOT show .env file
```

If `.env` appears, add it to `.gitignore`:
```bash
echo ".env" >> .gitignore
git add .gitignore
git commit -m "Add .env to gitignore"
```

## Getting Your Key

1. Visit: https://aistudio.google.com/app/apikey
2. Click "Create API key"
3. Copy it immediately (shown only once)
4. Paste into `.env` file or app sidebar
