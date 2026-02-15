# WE4Free Global - Country Onboarding Guide

**How to add mental health crisis resources for YOUR country**

---

## 🌍 Mission

**Universal access to mental health crisis support. Every country. Every language. Offline-capable.**

This guide will help you create a country configuration file that powers a free, offline-capable Progressive Web App (PWA) for mental health crisis resources.

---

## 📋 Table of Contents

1. [What Data You Need](#what-data-you-need)
2. [Creating Your Config File](#creating-your-config-file)
3. [Step-by-Step Walkthrough](#step-by-step-walkthrough)
4. [Validation Checklist](#validation-checklist)
5. [Submission Process](#submission-process)
6. [Data Sources](#data-sources)
7. [Multilingual Support](#multilingual-support)
8. [Examples](#examples)

---

## What Data You Need

### Minimum Required

✅ **Country Information:**
- Country name (English)
- ISO country code (2 letters, e.g., "CA" for Canada)
- Primary language(s) (e.g., ["en", "fr"])
- Emergency number (e.g., "911", "999", "112")
- Timezone (IANA format, e.g., "America/Toronto")

✅ **Crisis Lines (at least 1):**
- Line name
- Phone number
- Operating hours
- Brief description
- Whether it's free
- Whether it's confidential

### Recommended

🟡 **Additional Contact Methods:**
- SMS/text numbers
- Chat URLs
- Email addresses

🟡 **Demographic-Specific Lines:**
- Youth crisis lines
- LGBTQ+ support
- Veterans support
- Indigenous/cultural support
- Gender-specific lines

🟡 **Translations:**
- Site title in local languages
- Key phrases translated
- Crisis line descriptions in native languages

### Optional

⚪ **Additional Resources:**
- Mental health clinics
- Support groups
- Government services
- Emergency departments

⚪ **Customization:**
- Theme colors
- Logo/icons
- Custom fonts

---

## Creating Your Config File

### Step 1: Copy Template

**Start with the universal template:**

```bash
# Copy template to your country
copy we4free_global_config_template.json config_germany.json
```

**Or download template from:**
https://github.com/vortsghost2025/Deliberate-AI-Ensemble/blob/master/we4free_global_config_template.json

### Step 2: Fill in Country Metadata

**Edit country section:**

```json
{
  "country": {
    "code": "DE",
    "name": "Germany",
    "languages": ["de", "en"],
    "emergency_number": "112",
    "timezone": "Europe/Berlin"
  },
  "metadata": {
    "deployed_by": "Your Name or Organization",
    "contact_email": "contact@example.com",
    "last_updated": "2026-02-15",
    "site_url": ""
  }
}
```

**Country codes:** Use [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) (2 letters)  
**Timezones:** Use [IANA timezone database](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)

### Step 3: Add Crisis Lines

**For each crisis line, add an entry:**

```json
{
  "crisis_lines": [
    {
      "id": "telefonseelsorge",
      "name": "Telefonseelsorge",
      "description": "Free, anonymous crisis support available 24/7",
      "phone": "0800-111-0-111",
      "sms": "",
      "chat_url": "https://online.telefonseelsorge.de/",
      "email": "",
      "hours": "24/7",
      "languages": ["de"],
      "age_range": "",
      "free": true,
      "confidential": true
    },
    {
      "id": "kinder-jugendtelefon",
      "name": "Kinder- und Jugendtelefon",
      "description": "Support for children and youth",
      "phone": "116-111",
      "sms": "",
      "chat_url": "",
      "email": "",
      "hours": "Mon-Sat 2pm-8pm",
      "languages": ["de"],
      "age_range": "0-20",
      "free": true,
      "confidential": true
    }
  ]
}
```

**Field explanations:**

- **id:** Unique identifier (lowercase, no spaces, e.g., "german-crisis-line")
- **name:** Display name of the crisis line
- **description:** 1-2 sentences explaining who it supports
- **phone:** Phone number (include country code if international)
- **sms:** SMS/text number (if different from phone)
- **chat_url:** Web chat URL (if available)
- **email:** Email contact (if available)
- **hours:** Operating hours (use "24/7" or "Mon-Fri 9am-5pm" format)
- **languages:** Array of language codes ["de", "en"]
- **age_range:** Age restriction if any (e.g., "13-24", "0-18")
- **free:** Is the call/text free? (true/false)
- **confidential:** Is it confidential/anonymous? (true/false)

### Step 4: Add Translations (Optional but Recommended)

**For multilingual support:**

```json
{
  "translations": {
    "de": {
      "site_title": "Krisenhilfe Deutschland",
      "site_description": "Kostenlose, vertrauliche Krisenhilfe 24/7 verfügbar",
      "emergency_header": "⚠️ Lebensbedrohlicher Notfall",
      "emergency_description": "Bei akuter Gefahr Notruf wählen",
      "crisis_lines_header": "24/7 Krisentelefone",
      "crisis_lines_description": "Kostenlose, vertrauliche Unterstützung",
      "call_now": "Anrufen",
      "text_now": "SMS senden",
      "chat_now": "Chat starten",
      "offline_notice": "Sie sind offline. Alle Telefonnummern sind weiterhin erreichbar.",
      "footer_main": "Du bist nicht allein. Hilfe ist verfügbar.",
      "footer_disclaimer": "Dieser Service bietet nur Informationen. Bei akuter Gefahr rufen Sie sofort den Notruf."
    },
    "en": {
      "site_title": "Germany Crisis Support",
      "site_description": "Free, confidential crisis support available 24/7",
      "emergency_header": "⚠️ Life-Threatening Emergency",
      "emergency_description": "If you are in immediate danger, call emergency services"
    }
  }
}
```

**Translation keys:**
- `site_title` - Browser tab title
- `site_description` - Meta description / subtitle
- `emergency_header` - Emergency banner heading
- `emergency_description` - Emergency banner subtext
- `crisis_lines_header` - Crisis lines section heading
- `crisis_lines_description` - Crisis lines section intro
- `call_now` - Button text for phone
- `text_now` - Button text for SMS
- `chat_now` - Button text for chat
- `email` - Button text for email
- `offline_notice` - Message shown when offline
- `footer_main` - Main footer message
- `footer_disclaimer` - Disclaimer text

### Step 5: Customize Appearance (Optional)

**Set theme colors:**

```json
{
  "pwa_settings": {
    "name": "WE4Free Germany",
    "short_name": "Crisis DE",
    "description": "Free crisis support resources for Germany",
    "theme_color": "#000000",
    "background_color": "#FFFFFF",
    "display": "standalone",
    "orientation": "portrait",
    "start_url": "/",
    "scope": "/"
  },
  "customization": {
    "primary_color": "#E40303",
    "accent_color": "#FFED00",
    "danger_color": "#FF0000",
    "font_family": "system-ui, -apple-system, sans-serif",
    "logo_url": ""
  }
}
```

---

## Step-by-Step Walkthrough

### Example: Adding France 🇫🇷

**Step 1: Research Crisis Lines**

Search: "France suicide prevention hotline"

Found:
- **SOS Amitié:** 09 72 39 40 50 (24/7, French)
- **Suicide écoute:** 01 45 39 40 00 (24/7, French)
- **3114:** National suicide prevention number (24/7, French)
- **Fil Santé Jeunes:** 0 800 235 236 (Youth, 9am-11pm, French)

**Step 2: Create config_france.json**

```json
{
  "country": {
    "code": "FR",
    "name": "France",
    "languages": ["fr", "en"],
    "emergency_number": "15",
    "timezone": "Europe/Paris"
  },
  "metadata": {
    "deployed_by": "Community Contributor",
    "contact_email": "contributor@example.com",
    "last_updated": "2026-02-15",
    "site_url": ""
  },
  "crisis_lines": [
    {
      "id": "3114",
      "name": "3114 - Numéro National de Prévention du Suicide",
      "description": "Numéro national de prévention du suicide, écoute et soutien 24h/24",
      "phone": "3114",
      "sms": "",
      "chat_url": "",
      "email": "",
      "hours": "24/7",
      "languages": ["fr"],
      "age_range": "",
      "free": true,
      "confidential": true
    },
    {
      "id": "sos-amitie",
      "name": "SOS Amitié",
      "description": "Service d'écoute par téléphone, anonyme et gratuit",
      "phone": "09 72 39 40 50",
      "sms": "",
      "chat_url": "https://www.sos-amitie.com/",
      "email": "",
      "hours": "24/7",
      "languages": ["fr"],
      "age_range": "",
      "free": true,
      "confidential": true
    },
    {
      "id": "fil-sante-jeunes",
      "name": "Fil Santé Jeunes",
      "description": "Service d'écoute pour les jeunes de 12 à 25 ans",
      "phone": "0 800 235 236",
      "sms": "",
      "chat_url": "https://www.filsantejeunes.com/",
      "email": "",
      "hours": "Daily 9am-11pm",
      "languages": ["fr"],
      "age_range": "12-25",
      "free": true,
      "confidential": true
    }
  ],
  "resources": [],
  "translations": {
    "fr": {
      "site_title": "Soutien en Crise France",
      "site_description": "Ressources gratuites et confidentielles disponibles 24h/24",
      "emergency_header": "⚠️ Urgence Vitale",
      "emergency_description": "En cas de danger immédiat, appelez le SAMU",
      "crisis_lines_header": "Lignes d'Écoute 24/7",
      "crisis_lines_description": "Soutien gratuit et confidentiel disponible maintenant",
      "call_now": "Appeler",
      "text_now": "SMS",
      "chat_now": "Chat en ligne",
      "offline_notice": "Vous êtes hors ligne. Tous les numéros de téléphone restent accessibles.",
      "footer_main": "Vous n'êtes pas seul. De l'aide est disponible.",
      "footer_disclaimer": "Ce service fournit des informations uniquement. En cas d'urgence vitale, appelez immédiatement les services d'urgence."
    }
  },
  "pwa_settings": {
    "name": "WE4Free France",
    "short_name": "WE4Free",
    "description": "Ressources de soutien en crise gratuites",
    "theme_color": "#0055A4",
    "background_color": "#FFFFFF",
    "display": "standalone",
    "orientation": "portrait",
    "start_url": "/",
    "scope": "/"
  },
  "service_worker": {
    "cache_name": "we4free-france-v1",
    "cache_files": [
      "/",
      "/index.html",
      "/manifest.json"
    ],
    "offline_fallback": "/"
  },
  "analytics": {
    "enabled": false,
    "privacy_first": true,
    "no_personal_data": true
  },
  "customization": {
    "primary_color": "#0055A4",
    "accent_color": "#EF4135",
    "danger_color": "#EF4135",
    "font_family": "system-ui, -apple-system, sans-serif",
    "logo_url": ""
  }
}
```

**Step 3: Validate**

```bash
# Test build
cd we4free_global
node build.js ../config_france.json

# Check output
dir dist\FR
```

**Step 4: Submit**

See [Submission Process](#submission-process) below.

---

## Validation Checklist

Before submitting, verify:

### ✅ Required Fields
- [ ] Country code is 2 letters (ISO 3166-1 alpha-2)
- [ ] Country name is in English
- [ ] Emergency number is correct
- [ ] Timezone is valid IANA format
- [ ] At least 1 crisis line included
- [ ] All phone numbers tested/verified
- [ ] Hours of operation confirmed

### ✅ Data Quality
- [ ] Phone numbers are current (checked within 30 days)
- [ ] URLs are working (no 404 errors)
- [ ] Crisis line descriptions are accurate
- [ ] Free/confidential status confirmed
- [ ] Language support verified
- [ ] Age restrictions noted if any

### ✅ Translations (if included)
- [ ] Primary language translations complete
- [ ] Translations reviewed by native speaker
- [ ] No machine translation placeholders
- [ ] Special characters handled correctly (é, ñ, ü, etc.)

### ✅ Build Test
- [ ] Build runs without errors
- [ ] Generated HTML displays correctly
- [ ] Phone links work on mobile
- [ ] SMS links work on mobile
- [ ] Chat URLs open correctly
- [ ] Offline mode works

---

## Submission Process

### Option 1: GitHub Pull Request (Recommended)

**For developers:**

```bash
# 1. Fork the repository
# Go to https://github.com/vortsghost2025/Deliberate-AI-Ensemble
# Click "Fork"

# 2. Clone your fork
git clone https://github.com/YOUR-USERNAME/Deliberate-AI-Ensemble.git
cd Deliberate-AI-Ensemble

# 3. Add your config
copy config_yourCountry.json .

# 4. Test build
cd we4free_global
node build.js ..\config_yourCountry.json

# 5. Commit and push
git add config_yourCountry.json
git commit -m "Add [Country] crisis resources"
git push origin master

# 6. Create Pull Request
# Go to your fork on GitHub
# Click "Pull Request"
# Submit!
```

### Option 2: Email Submission

**For non-developers:**

1. **Create your config file** following this guide
2. **Test locally** (optional, but recommended)
3. **Email to:** ai@deliberateensemble.works
   - Subject: "WE4Free Country Submission - [Country Name]"
   - Attach: `config_yourCountry.json`
   - Include: Name, organization (if any), contact email
4. **We will review** and deploy within 1 week

### Option 3: GitHub Issue

**Quick submission:**

1. Go to [GitHub Issues](https://github.com/vortsghost2025/Deliberate-AI-Ensemble/issues)
2. Click "New Issue"
3. Title: "Country Config: [Country Name]"
4. Paste your JSON config
5. Submit!

---

## Data Sources

### Trusted Sources for Crisis Line Information

**International:**
- **International Association for Suicide Prevention (IASP):** https://www.iasp.info/resources/Crisis_Centres/
- **Befrienders Worldwide:** https://www.befrienders.org/
- **Wikipedia List of Suicide Crisis Lines:** https://en.wikipedia.org/wiki/List_of_suicide_crisis_lines

**By Country:**
- Government health ministry websites
- National mental health organizations
- Crisis line network websites
- Verified NGO sources

**Verification Process:**
1. Check government health websites first
2. Cross-reference with 2+ sources
3. Call the number to verify it works
4. Confirm operating hours
5. Document date of verification

---

## Multilingual Support

### Adding Multiple Languages

**Example: Canada (English + French)**

```json
{
  "country": {
    "languages": ["en", "fr"]
  },
  "crisis_lines": [
    {
      "name": "Canada Suicide Prevention Service",
      "description": "Free, confidential support available 24/7",
      "languages": ["en", "fr"]
    }
  ],
  "translations": {
    "en": {
      "site_title": "Canada Crisis Support",
      "crisis_lines_header": "24/7 Crisis Lines"
    },
    "fr": {
      "site_title": "Soutien en Crise Canada",
      "crisis_lines_header": "Lignes de Crise 24/7"
    }
  }
}
```

**Primary language:** First in `languages` array (e.g., "en" in ["en", "fr"])

**Fallback:** If translation missing, English is used

---

## Examples

### Large Country (Multiple Regions)

**Example: India (Multiple Languages, Regional Lines)**

```json
{
  "country": {
    "code": "IN",
    "name": "India",
    "languages": ["en", "hi"],
    "emergency_number": "112",
    "timezone": "Asia/Kolkata"
  },
  "crisis_lines": [
    {
      "id": "kiran-national",
      "name": "KIRAN Mental Health Helpline",
      "description": "National mental health helpline",
      "phone": "1800-599-0019",
      "languages": ["en", "hi"],
      "hours": "24/7"
    },
    {
      "id": "sumaitri-delhi",
      "name": "SUMAITRI (Delhi)",
      "description": "Crisis intervention center in Delhi",
      "phone": "011-23389090",
      "languages": ["en", "hi"],
      "hours": "2pm-10pm"
    },
    {
      "id": "aasra-mumbai",
      "name": "Aasra (Mumbai)",
      "description": "Crisis helpline in Mumbai",
      "phone": "91-9820466726",
      "email": "aasrahelpline@yahoo.com",
      "languages": ["en", "hi", "mr"],
      "hours": "24/7"
    }
  ]
}
```

### Small Country (Single Line)

**Example: Iceland**

```json
{
  "country": {
    "code": "IS",
    "name": "Iceland",
    "languages": ["is", "en"],
    "emergency_number": "112",
    "timezone": "Atlantic/Reykjavik"
  },
  "crisis_lines": [
    {
      "id": "rodin-raudilinja",
      "name": "Rauði Krossinn (Red Cross)",
      "description": "Crisis support and counseling",
      "phone": "1717",
      "chat_url": "https://www.1717.is/",
      "hours": "Daily 6pm-2am",
      "languages": ["is", "en"],
      "free": true,
      "confidential": true
    }
  ]
}
```

### Developing Country (Limited Services)

**Example: Nepal**

```json
{
  "country": {
    "code": "NP",
    "name": "Nepal",
    "languages": ["ne", "en"],
    "emergency_number": "112",
    "timezone": "Asia/Kathmandu"
  },
  "crisis_lines": [
    {
      "id": "transcultural-psychosocial",
      "name": "Transcultural Psychosocial Organization (TPO Nepal)",
      "description": "Mental health and psychosocial support",
      "phone": "01-4102037",
      "hours": "Sun-Fri 9am-5pm",
      "languages": ["ne", "en"],
      "free": false,
      "confidential": true
    }
  ]
}
```

**Note:** Even limited services provide value. Start with what's available, community can expand later.

---

## Next Steps

✅ **Created your config?**
- Submit via [GitHub PR](#option-1-github-pull-request-recommended) or [email](#option-2-email-submission)
- Build and test locally: `node build.js config_yourCountry.json`
- Deploy to test: See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

✅ **Need help?**
- Open an issue: [GitHub Issues](https://github.com/vortsghost2025/Deliberate-AI-Ensemble/issues)
- Email: ai@deliberateensemble.works
- Join discussion: [GitHub Discussions](https://github.com/vortsghost2025/Deliberate-AI-Ensemble/discussions)

✅ **Want to contribute more?**
- Translate existing configs
- Verify/update crisis line information
- Help with testing and validation
- Spread the word in your country!

---

**Thank you for contributing to universal mental health access. Every country matters. Every life matters. 💙🌍**

**For WE. For everyone.**

**License:** MIT (free for any use)  
**Repository:** https://github.com/vortsghost2025/Deliberate-AI-Ensemble  
**Research:** https://doi.org/10.17605/OSF.IO/N3TYA
