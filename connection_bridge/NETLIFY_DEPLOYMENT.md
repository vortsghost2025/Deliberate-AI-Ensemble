# 🌱 WE4Free Connection Bridge - Netlify Deployment Guide

## 🚀 Quick Deployment Steps

### 1. Add Environment Variable to Netlify
To enable Bitly link shortening on the live site, you need to add your Bitly token to Netlify:

1. Go to your Netlify dashboard: https://app.netlify.com
2. Select your `we4free` site
3. Click **Site settings** (in the top navigation)
4. In the left sidebar, click **Environment variables**
5. Click **Add a variable**
   - **Key**: `BITLY_TOKEN`
   - **Value**: `cfaed30fff4feeb3bf6282ee9abc4161497e9eb3`
6. Click **Save**

### 2. Deploy Updated Files
1. Open **File Explorer** (Windows Explorer)
2. Navigate to `c:\workspace\connection_bridge`
3. Go to https://app.netlify.com/drop
4. Drag the entire `connection_bridge` folder onto the Netlify deploy area
5. Wait 30-60 seconds for deployment to complete

### 3. Test the Live Site
1. Visit your live site: https://we4free.netlify.app
2. Create a test message
3. Verify that the shortened link starts with `bit.ly/`
4. Click the generated link to confirm the message displays correctly

---

## 🔧 How It Works

### Local Development
- Uses `server.js` Node.js server
- Bitly API calls handled by `/api/shorten` endpoint
- Run with: `node server.js`
- Access at: http://localhost:3000

### Live Netlify Site
- Uses serverless function at `netlify/functions/shorten.js`
- Bitly API calls handled by `/.netlify/functions/shorten` endpoint
- Automatically detects hostname and uses correct endpoint
- Environment variables set in Netlify dashboard

---

## 📁 File Structure
```
connection_bridge/
├── index.html              # Main form page
├── receive.html           # Message display page
├── server.js              # Local development server
├── netlify.toml           # Netlify configuration
├── .env                   # Local environment (gitignored)
└── netlify/
    └── functions/
        └── shorten.js     # Netlify serverless function
```

---

## 💙 Built with WE4Free
"in life it doesn't matter where you go its who you go there with"
