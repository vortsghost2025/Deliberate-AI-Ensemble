# Deploy Your Own WE4Free Mental Health Resources Site 🆘💙

**This is 100% FREE. No coding experience needed.**

## Why Deploy Your Own?

- Customize for YOUR community's crisis resources
- Add resources in YOUR language
- Make it available to YOUR community
- Help more people access crisis support offline

---

## ⚡ Quick Deploy (Choose One)

### Option 1: GitHub Pages (Easiest - 5 minutes)

**Perfect for: Anyone with a GitHub account**

1. **Fork this repository:**
   - Click "Fork" button at top of GitHub page
   - Creates your own copy

2. **Enable GitHub Pages:**
   - Go to your fork's Settings
   - Click "Pages" in left sidebar
   - Source: "Deploy from a branch"
   - Branch: Select "master"
   - Folder: Select "/we4free_website"
   - Click "Save"

3. **Your site is live!**
   - URL will be: `https://yourusername.github.io/Deliberate-AI-Ensemble/`
   - Takes 2-3 minutes to build first time

**Cost: $0 forever**

---

### Option 2: Netlify (Auto-updates when you make changes)

**Perfect for: Automatic deployments + custom domain**

1. **Sign up:** Go to [netlify.com](https://netlify.com) (free account)

2. **New site:**
   - Click "Add new site" → "Import an existing project"
   - Choose "GitHub" 
   - Authorize Netlify
   - Select your forked repository

3. **Configure:**
   - Base directory: `we4free_website`
   - Build command: (leave empty)
   - Publish directory: `.`
   - Click "Deploy site"

4. **Your site is live!**
   - Netlify gives you a random URL
   - Can change to custom name: "Settings" → "Change site name"
   - Example: `your-crisis-resources.netlify.app`

**Cost: $0 forever**

---

### Option 3: Vercel (Fastest global performance)

**Perfect for: Maximum speed worldwide**

1. **Sign up:** Go to [vercel.com](https://vercel.com) (free account)

2. **Import:**
   - Click "Add New..." → "Project"
   - Import Git Repository → Select your fork
   - Authorize Vercel

3. **Configure:**
   - Framework Preset: "Other"
   - Root Directory: `we4free_website`
   - Leave build settings default
   - Click "Deploy"

4. **Your site is live!**
   - Vercel gives you a `.vercel.app` URL
   - Can add custom domain for free

**Cost: $0 forever**

---

### Option 4: Cloudflare Pages (Cloudflare's global CDN)

**Perfect for: Maximum reliability + speed**

1. **Sign up:** Go to [pages.cloudflare.com](https://pages.cloudflare.com)

2. **Connect:**
   - Click "Create a project"
   - Connect to Git → GitHub
   - Select your forked repository

3. **Configure:**
   - Production branch: `master`
   - Build command: (leave empty)
   - Build output directory: `/we4free_website`
   - Click "Save and Deploy"

4. **Your site is live!**
   - Gets a `.pages.dev` URL
   - Can add custom domain

**Cost: $0 forever**

---

## 🖥️ Test Locally First (Optional)

**If you want to test changes before deploying:**

```bash
# Clone the repository
git clone https://github.com/vortsghost2025/Deliberate-AI-Ensemble.git
cd Deliberate-AI-Ensemble/we4free_website

# Serve locally (Python 3)
python -m http.server 8080

# OR with Node.js
npx http-server -p 8080

# Visit: http://localhost:8080
```

**Test offline mode:**
1. Visit site in browser
2. Open DevTools (F12)
3. Go to "Application" tab → "Service Workers"
4. Check "Offline" checkbox
5. Refresh page - should still work!

---

## 🎨 Customize For Your Community

### 1. Update Crisis Numbers

Edit `resources.html`:

```html
<!-- Find the crisis box section -->
<div class="crisis-box">
    <!-- Replace with YOUR region's numbers -->
    <p class="crisis-contact">🆘 <strong>Emergency:</strong> 911</p>
    <p class="crisis-contact">📞 <strong>Crisis:</strong> 988</p>
    <!-- Add more... -->
</div>
```

### 2. Add Your Region's Resources

In `resources.html`, add a new province/state section:

```html
<div class="resource-section" id="your-region">
    <h3>🏠 Your Region Name</h3>
    <div class="resource-item">
        <h4>Crisis Center Name</h4>
        <p>📞 Phone: 1-800-XXX-XXXX</p>
        <p>💬 Text: XXX-XXX</p>
        <p>🌐 Website: <a href="https://example.com">example.com</a></p>
    </div>
</div>
```

### 3. Update Service Worker Cache

**Important:** When you make changes, update cache version in `sw.js`:

```javascript
// Change version number
const CACHE_NAME = 'we4free-v11'; // Increment this!
```

### 4. Translate to Another Language

1. Copy all HTML files
2. Translate the text content
3. Update `<html lang="en">` to your language code
4. Update `manifest.json` → `lang` property

---

## 📱 Share Your Deployment

Once live, share everywhere:

**Print QR codes for:**
- Community centers
- Libraries
- Schools
- Support group meetings
- Doctor's offices
- Shelters

**Share on social media:**
- Include your custom URL
- Tag local mental health organizations
- Use hashtags: #MentalHealth #CrisisSupport

**Email to:**
- Local mental health organizations
- School counselors
- Community leaders
- Support groups

---

## ✅ Verify It Works Offline

**Test checklist:**

1. ✅ Visit your deployed site
2. ✅ Open browser DevTools (F12)
3. ✅ Check "Application" → "Service Workers" → See "Activated"
4. ✅ Check "Application" → "Cache Storage" → See cached files
5. ✅ Enable "Offline" mode in DevTools
6. ✅ Refresh page - should still load
7. ✅ Check that crisis numbers are visible

**If offline mode doesn't work:**
- Clear browser cache and try again
- Check service worker is registered (console messages)
- Make sure HTTPS is enabled (required for PWA)

---

## 🆘 Need Help?

**Issues Deploying?**
- Open an issue on GitHub: [Issues](https://github.com/vortsghost2025/Deliberate-AI-Ensemble/issues)
- Include: platform used, error messages, screenshots

**Questions About Customization?**
- Check existing issues first
- Open a new issue with your question
- Community will help!

**Want to Contribute?**
- Fork the repo
- Make your improvements
- Submit a Pull Request
- Help others in issues

---

## 💙 You're Making a Difference

By deploying this, you're:

✅ Making crisis support accessible offline  
✅ Breaking down barriers to mental health help  
✅ Helping your community in tangible ways  
✅ Contributing to open source mental health resources  

**Every deployment helps someone.**

---

## 📊 Track Impact (Optional)

If you want to see how many people are using your deployment:

**Free analytics options:**
- [Plausible Analytics](https://plausible.io) (privacy-focused, free tier)
- [GoatCounter](https://www.goatcounter.com) (privacy-focused, free)
- Simple Access Logs (if self-hosting)

**No Google Analytics please** - keep it privacy-respecting 💙

---

## 🎯 Next Steps

1. ✅ Deploy using one of the options above
2. ✅ Verify offline mode works
3. ✅ Customize for your region
4. ✅ Share with your community
5. ✅ Print QR codes for physical locations
6. ✅ Update resources regularly

---

**For everyone. For WE. 💙🫡**

---

## License

MIT License - Do whatever you want with this.  
Make it better. Share it. Save lives.

**No attribution required. Just help people.**
