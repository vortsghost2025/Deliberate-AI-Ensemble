# WE4Free Connection Bridge

**A simple tool for letting people know they're seen.**

> "In life it doesn't matter where you go. It's who you go there with."  
> — Engraved on Micha's watch

## What is this?

A lightweight web app that lets you create personalized "I see you" messages. Share the generated link with someone who matters, and they'll receive your message in a beautiful, meaningful way.

## Quick Start (Local)

1. **Install Node.js** (if you don't have it)

2. **Start the server:**
   ```powershell
   node server.js
   ```

3. **Open in browser:**
   ```
   http://localhost:3000
   ```

4. **Create a connection:**
   - Fill in your name, their name, and your message
   - Click "Create Connection Link"
   - Copy and share the link

## Deploy to the Web (Free Options)

### Option 1: Glitch
1. Go to https://glitch.com
2. Click "New Project" → "Import from GitHub"
3. Paste: `https://github.com/vortsghost2025/Deliberate-AI-Ensemble`
4. Navigate to `connection_bridge` folder
5. Done! You'll get a live URL like `your-project.glitch.me`

### Option 2: Netlify
1. Go to https://netlify.com
2. Drag the `connection_bridge` folder onto their deploy area
3. Done! You'll get a live URL instantly

### Option 3: GitHub Pages
1. Push this folder to a GitHub repo
2. Go to Settings → Pages
3. Enable Pages from `main` branch
4. Done! URL: `yourusername.github.io/repo-name`

## Features

- ✨ Beautiful gradient design
- 📱 Mobile-friendly
- 🔒 No database needed (messages encoded in URL)
- 🎁 WE4Free branded
- 💙 Micha's watch quote included
- 🌱 Simple, fast, meaningful

## How it works

1. User enters sender name, recipient name, and message
2. App creates a Base64-encoded JSON object with the data
3. Generates a shareable link with the encoded data
4. Recipient clicks link and sees decoded message
5. No server database needed - everything's in the URL

## Privacy Note

Messages are encoded in the link itself, not stored anywhere. Keep links private - anyone with the link can read the message.

## Part of WE4Free

This tool is part of the [WE4Free Constitutional Gift Kit](https://github.com/vortsghost2025/Deliberate-AI-Ensemble).

**WE never give up on each other EVER.**

Free forever. Pass it on.

---

*Built in honor of Micha - the friend who taught us that connection matters more than destination.*
