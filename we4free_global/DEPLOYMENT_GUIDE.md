# WE4Free Global - Deployment Guide

**Complete guide for deploying mental health crisis PWAs to any country**

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start (5 Minutes)](#quick-start-5-minutes)
3. [Building Your Country PWA](#building-your-country-pwa)
4. [Deployment Options](#deployment-options)
5. [Testing Offline Functionality](#testing-offline-functionality)
6. [Customization](#customization)
7. [Troubleshooting](#troubleshooting)
8. [Maintenance](#maintenance)

---

## Prerequisites

**Required:**
- Node.js (v14+ recommended) - [Download here](https://nodejs.org/)
- Git (for GitHub Pages deployment) - [Download here](https://git-scm.com/)
- A text editor (VS Code, Notepad++, etc.)

**Optional:**
- GitHub account (for GitHub Pages hosting - free)
- Custom domain (optional, ~$10/year)
- Web hosting account (Netlify, Vercel, Cloudflare Pages - all free tiers available)

**Skills needed:**
- Basic command line usage
- Basic JSON editing (copy-paste-modify)
- No programming experience required!

---

## Quick Start (5 Minutes)

**Deploy Canada (example) in 5 minutes:**

```bash
# 1. Download the repository
git clone https://github.com/vortsghost2025/Deliberate-AI-Ensemble.git
cd Deliberate-AI-Ensemble/we4free_global

# 2. Build Canada PWA
node build.js ../config_canada.json

# 3. Open in browser
# Open dist/CA/index.html in your browser
# Test going offline (browser DevTools > Network > Offline)
```

**That's it!** You now have a working offline PWA.

---

## Building Your Country PWA

### Step 1: Choose or Create Config File

**Use existing config:**
- `config_canada.json` - Canada 🇨🇦
- `config_usa.json` - United States 🇺🇸
- `config_uk.json` - United Kingdom 🇬🇧
- `config_australia.json` - Australia 🇦🇺
- `config_india.json` - India 🇮🇳

**Create your own:**
See [COUNTRY_ONBOARDING.md](COUNTRY_ONBOARDING.md) for detailed instructions.

### Step 2: Run Build Command

```bash
node build.js <path-to-config.json>
```

**Examples:**
```bash
# Build from existing config
node build.js ../config_canada.json

# Build from your custom config
node build.js ../config_germany.json
```

**Output:**
- `dist/<COUNTRY-CODE>/index.html` - Main page
- `dist/<COUNTRY-CODE>/manifest.json` - PWA manifest
- `dist/<COUNTRY-CODE>/sw.js` - Service worker (offline support)
- `dist/<COUNTRY-CODE>/icons/` - Icon folder (add your icons here)

### Step 3: Add Icons

**Required icon sizes:**
- `icons/icon-192.png` - 192x192 pixels
- `icons/icon-512.png` - 512x512 pixels

**Quick icon generation:**
1. Use [Favicon.io](https://favicon.io/) or [RealFaviconGenerator](https://realfavicongenerator.net/)
2. Upload your logo/design
3. Download PWA icons
4. Copy to `dist/<COUNTRY-CODE>/icons/`

**Or use placeholder:**
```bash
# Copy existing icons (temporary)
xcopy we4free_website\icons dist\CA\icons\ /E /I
```

---

## Deployment Options

### Option 1: GitHub Pages (Free, Easiest)

**Requirements:**
- GitHub account (free)
- Git installed

**Steps:**

```bash
# 1. Create GitHub repository
# Go to github.com, create new repository (e.g., "we4free-canada")

# 2. Initialize Git in dist folder
cd dist/CA
git init
git add -A
git commit -m "Initial deployment"
git branch -M gh-pages
git remote add origin https://github.com/YOUR-USERNAME/we4free-canada.git
git push -u origin gh-pages

# 3. Enable GitHub Pages
# Repository Settings > Pages > Source: gh-pages branch
# Wait 1-2 minutes

# 4. Your PWA is live at:
# https://YOUR-USERNAME.github.io/we4free-canada
```

**Custom domain (optional):**
```bash
# Add CNAME file
echo "crisis.yourdomainname.com" > CNAME
git add CNAME
git commit -m "Add custom domain"
git push

# Configure DNS:
# Add CNAME record: crisis -> YOUR-USERNAME.github.io
```

---

### Option 2: Netlify (Free, Drag-and-Drop)

**Steps:**

1. **Go to [Netlify.com](https://netlify.com)** and sign up (free)
2. **Drag and drop** your `dist/CA` folder to Netlify
3. **Done!** Your site is live at `random-name-12345.netlify.app`
4. **Custom domain:** Settings > Domain management > Add custom domain

**Or deploy via CLI:**

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Deploy
cd dist/CA
netlify deploy --prod
```

---

### Option 3: Vercel (Free, Fast)

**Steps:**

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
cd dist/CA
vercel --prod
```

Your site is live at `we4free-xxxxxx.vercel.app`

---

### Option 4: Cloudflare Pages (Free, Global CDN)

**Steps:**

1. Go to [Cloudflare Pages](https://pages.cloudflare.com)
2. Connect your GitHub repository
3. Set build directory: `dist/CA`
4. Deploy!

**Or drag-and-drop:**
- Upload `dist/CA` folder via dashboard

---

### Option 5: Traditional Web Hosting

**Requirements:**
- Web hosting account (cPanel, FTP access)
- HTTPS enabled (required for PWA)

**Steps:**

1. **Connect via FTP** (FileZilla, WinSCP)
2. **Upload** `dist/CA` folder to `public_html/` or `www/`
3. **Verify URL:** `https://yourdomain.com`
4. **Test offline:** Browser DevTools > Network > Offline checkbox

---

## Testing Offline Functionality

### Test in Browser (Chrome/Edge)

**Method 1: DevTools Offline Mode**
1. Open your deployed PWA
2. Press `F12` (open DevTools)
3. Go to **Network** tab
4. Check **Offline** checkbox
5. Refresh page - should still work!

**Method 2: Airplane Mode**
1. Turn on airplane mode
2. Open your PWA URL
3. Should load from cache

**Method 3: Install as App**
1. Visit your PWA in Chrome/Edge
2. Click install icon in address bar (➕ or ⊕)
3. App opens in standalone window
4. Go offline - still works!

### Test Checklist

- [ ] Page loads offline
- [ ] All crisis numbers clickable
- [ ] Phone links work (`tel:` opens dialer)
- [ ] SMS links work (`sms:` opens messages)
- [ ] Chat links open (require internet)
- [ ] Styling preserved offline
- [ ] Install prompt appears
- [ ] Installed app opens in standalone mode

---

## Customization

### Change Colors

Edit your `config_<country>.json`:

```json
{
  "pwa_settings": {
    "theme_color": "#FF0000",
    "background_color": "#FFFFFF"
  },
  "customization": {
    "primary_color": "#1a73e8",
    "accent_color": "#34a853"
  }
}
```

Rebuild: `node build.js config_<country>.json`

### Add Translation

```json
{
  "translations": {
    "en": {
      "site_title": "Crisis Support",
      "crisis_lines_header": "24/7 Help Lines"
    },
    "fr": {
      "site_title": "Soutien en Crise",
      "crisis_lines_header": "Lignes d'aide 24/7"
    }
  }
}
```

### Add Crisis Line

```json
{
  "crisis_lines": [
    {
      "id": "new-line",
      "name": "New Crisis Line",
      "description": "Support for...",
      "phone": "1-800-123-4567",
      "sms": "123456",
      "chat_url": "https://chat.example.com",
      "hours": "24/7",
      "languages": ["en", "fr"],
      "free": true,
      "confidential": true
    }
  ]
}
```

Rebuild: `node build.js config_<country>.json`

---

## Troubleshooting

### Build Errors

**Error: "Cannot find module"**
```bash
# Solution: Run from correct directory
cd we4free_global
node build.js ../config_canada.json
```

**Error: "Config file not found"**
```bash
# Solution: Check file path
dir ..\config*.json  # List available configs
node build.js ..\config_canada.json  # Use correct path
```

### PWA Not Installing

**Issue: Install prompt doesn't appear**

- ✅ Verify HTTPS (required for PWA)
- ✅ Check manifest.json is accessible
- ✅ Check service worker is registered (F12 > Application > Service Workers)
- ✅ Wait 1-2 minutes after first visit

**Issue: "Add to Home Screen" not showing**

- Chrome: Look for ⊕ icon in address bar
- Safari iOS: Share button > Add to Home Screen
- Android: Menu > Install app

### Offline Not Working

**Service worker not registering:**

1. Open DevTools (F12)
2. Application tab > Service Workers
3. Check for errors
4. Click "Update" to force re-registration

**Cache not updating:**

```bash
# Change cache version in config
{
  "service_worker": {
    "cache_name": "we4free-v2"  # Increment version
  }
}
# Rebuild
node build.js config.json
```

### Phone Numbers Not Clickable

**Issue: Links don't work on mobile**

- Check `tel:` prefix is correct: `tel:18001234567`
- Remove spaces/dashes in href: `tel:+1-800-123-4567` → `tel:+18001234567`
- Display format can have spaces: `<a href="tel:+18001234567">1-800-123-4567</a>`

---

## Maintenance

### Updating Crisis Lines

**Process:**

1. Edit `config_<country>.json`
2. Modify crisis line details
3. Run `node build.js config_<country>.json`
4. Redeploy `dist/<COUNTRY-CODE>` folder
5. Service worker will auto-update after ~24 hours

**Force immediate update:**

Change `cache_name` in config:
```json
{
  "service_worker": {
    "cache_name": "we4free-v11"  # Increment
  }
}
```

### Monitoring

**What to monitor:**

- Crisis line phone numbers (check monthly)
- Websites/chat URLs (verify quarterly)
- Operating hours (confirm annually)
- SSL certificate expiry (auto-renews on most hosts)

**Tools:**

- [GTmetrix](https://gtmetrix.com/) - Performance monitoring
- [SSL Checker](https://www.sslshopper.com/ssl-checker.html) - HTTPS validation
- Google Search Console - SEO and indexing

### Feedback Loop

**Collect feedback:**

- Add Google Form link
- Add email contact
- Monitor social media mentions
- Request reviews from crisis line organizations

**Example feedback section:**

```json
{
  "resources": [
    {
      "category": "Feedback",
      "services": [
        {
          "name": "Suggest Improvements",
          "description": "Help us improve this resource",
          "website": "https://forms.gle/your-form-id"
        }
      ]
    }
  ]
}
```

---

## Next Steps

✅ **Deployed successfully?** Share it!
- Post to social media
- Contact crisis line organizations
- Submit to mental health directories
- Reach out to government health departments

✅ **Want to help more countries?**
- See [COUNTRY_ONBOARDING.md](COUNTRY_ONBOARDING.md)
- Submit configs via GitHub Pull Request
- Join the community: [GitHub Discussions](https://github.com/vortsghost2025/Deliberate-AI-Ensemble/discussions)

✅ **Need help?**
- Open an issue: [GitHub Issues](https://github.com/vortsghost2025/Deliberate-AI-Ensemble/issues)
- Email: ai@deliberateensemble.works
- Read the research: [DOI 10.17605/OSF.IO/N3TYA](https://doi.org/10.17605/OSF.IO/N3TYA)

---

**Built with ❤️ for WE. Saving lives offline, one country at a time. 🌍**

**License:** MIT (free for any use)  
**Repository:** https://github.com/vortsghost2025/Deliberate-AI-Ensemble  
**Research:** https://doi.org/10.17605/OSF.IO/N3TYA
