#!/usr/bin/env node

/**
 * WE4Free Global - Country PWA Builder
 * 
 * Converts a country config JSON into a complete offline-capable PWA
 * Zero dependencies, pure Node.js
 * 
 * Usage: node build.js <country-config.json> [output-dir]
 */

const fs = require('fs');
const path = require('path');
const ConfigValidator = require('./validate.js');

// Load country config
function loadConfig(configPath) {
  try {
    const configData = fs.readFileSync(configPath, 'utf8');
    return JSON.parse(configData);
  } catch (error) {
    console.error(`❌ Error loading config: ${error.message}`);
    process.exit(1);
  }
}

// Validate config before building
function validateConfig(configPath) {
  const validator = new ConfigValidator();
  const result = validator.validate(configPath);
  
  if (!result.valid) {
    console.error('❌ Config validation failed:\n');
    result.errors.forEach(error => {
      console.error(`   ❌ ${error}`);
    });
    if (result.warnings.length > 0) {
      console.log('\n⚠️  Warnings:');
      result.warnings.forEach(warning => {
        console.log(`   ⚠️  ${warning}`);
      });
    }
    console.error('\n🛑 Build aborted. Fix errors and try again.');
    process.exit(1);
  }
  
  if (result.warnings.length > 0) {
    console.log('⚠️  Config has warnings (build will continue):\n');
    result.warnings.forEach(warning => {
      console.log(`   ⚠️  ${warning}`);
    });
    console.log('');
  }
  
  return result;
}

// Simple template engine (replace {{key}} with values)
function renderTemplate(template, data) {
  return template.replace(/\{\{([^}]+)\}\}/g, (match, key) => {
    const keys = key.trim().split('.');
    let value = data;
    for (const k of keys) {
      value = value?.[k];
    }
    return value !== undefined ? value : match;
  });
}

// Generate crisis lines HTML
function generateCrisisLinesHTML(crisisLines, translations) {
  return crisisLines.map(line => {
    const languageTags = line.languages ? 
      `<div class="languages">${line.languages.map(lang => `<span class="language-tag">${lang.toUpperCase()}</span>`).join('')}</div>` : '';
    
    return `
    <div class="crisis-line">
      <h3>${line.name}</h3>
      <p>${line.description}</p>
      <div class="contact-methods">
        ${line.phone ? `<a href="tel:${line.phone}" class="btn btn-primary">📞 ${translations.call_now || 'Call'} ${line.phone}</a>` : ''}
        ${line.sms ? `<a href="sms:${line.sms}" class="btn btn-secondary">💬 ${translations.text_now || 'Text'} ${line.sms}</a>` : ''}
        ${line.chat_url ? `<a href="${line.chat_url}" class="btn btn-tertiary" target="_blank" rel="noopener">💻 ${translations.chat_now || 'Chat Online'}</a>` : ''}
        ${line.email ? `<a href="mailto:${line.email}" class="btn btn-secondary">✉️ ${translations.email || 'Email'}</a>` : ''}
      </div>
      <p class="hours">${line.hours}${line.free !== false ? ' • Free & Confidential' : ''}</p>
      ${languageTags}
    </div>
  `;
  }).join('\n');
}

// Generate resources HTML
function generateResourcesHTML(resources) {
  return resources.map(category => `
    <div class="resource-category">
      <h3>${category.category}</h3>
      ${category.services.map(service => `
        <div class="service">
          <h4>${service.name}</h4>
          <p>${service.description || ''}</p>
          ${service.phone ? `<p>📞 ${service.phone}</p>` : ''}
          ${service.website ? `<p>🌐 <a href="${service.website}" target="_blank">${service.website}</a></p>` : ''}
          ${service.hours ? `<p>🕐 ${service.hours}</p>` : ''}
        </div>
      `).join('\n')}
    </div>
  `).join('\n');
}

// Generate manifest.json
function generateManifest(config) {
  const manifest = {
    name: config.pwa_settings?.name || `WE4Free ${config.country.name}`,
    short_name: config.pwa_settings?.short_name || `WE4Free`,
    description: config.pwa_settings?.description || "Free offline crisis support resources",
    start_url: "/",
    display: "standalone",
    background_color: config.pwa_settings?.background_color || "#ffffff",
    theme_color: config.pwa_settings?.theme_color || "#1a73e8",
    icons: [
      {
        src: "/icons/icon-192.png",
        sizes: "192x192",
        type: "image/png"
      },
      {
        src: "/icons/icon-512.png",
        sizes: "512x512",
        type: "image/png"
      }
    ]
  };
  return JSON.stringify(manifest, null, 2);
}

// Generate service worker
function generateServiceWorker(config) {
  const cacheName = config.service_worker?.cache_name || 'we4free-v1';
  const cacheFiles = config.service_worker?.cache_files || [
    '/',
    '/emergency.html',
    '/resources.html',
    '/manifest.json'
  ];

  return `
const CACHE_NAME = '${cacheName}';
const URLS_TO_CACHE = ${JSON.stringify(cacheFiles, null, 2)};

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(URLS_TO_CACHE))
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then((response) => response || fetch(event.request))
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});
`;
}

// Generate index.html from template
function generateIndexHTML(config) {
  const lang = config.country.languages[0] || 'en';
  const translations = config.translations?.[lang] || {};
  
  // Load template
  const templatePath = path.join(__dirname, 'templates', 'index.html');
  let template = fs.readFileSync(templatePath, 'utf8');
  
  // Prepare replacements
  const replacements = {
    lang: lang,
    site_title: translations.site_title || `${config.country.name} Crisis Support`,
    site_description: translations.site_description || 'Free, confidential crisis support available 24/7',
    theme_color: config.pwa_settings?.theme_color || '#1a73e8',
    country_name: config.country.name,
    emergency_header: translations.emergency_header || '⚠️ Life-Threatening Emergency',
    emergency_description: translations.emergency_description || 'If you are in immediate danger, call emergency services',
    emergency_number: config.country.emergency_number,
    offline_notice: translations.offline_notice || 'You are offline. All crisis numbers are still accessible.',
    crisis_lines_header: translations.crisis_lines_header || '24/7 Crisis Lines',
    crisis_lines_description: translations.crisis_lines_description || 'Free, confidential support available now',
    crisis_lines: generateCrisisLinesHTML(config.crisis_lines, translations),
    footer_main: translations.footer_main || 'You are not alone. Help is available.',
    footer_disclaimer: translations.footer_disclaimer || 'This service provides information only. In life-threatening emergencies, call emergency services immediately.'
  };
  
  // Replace all placeholders
  for (const [key, value] of Object.entries(replacements)) {
    const regex = new RegExp(`\\{\\{${key}\\}\\}`, 'g');
    template = template.replace(regex, value || '');
  }
  
  return template;
}

// Main build function
function build(configPath, outputDir = 'dist') {
  console.log('🌍 WE4Free Global Builder v1.0.0');
  console.log(`📁 Loading config: ${configPath}`);
  
  // PHASE 5: Validate before building
  console.log('🔍 Validating config...');
  validateConfig(configPath);
  console.log('✅ Config valid\n');
  
  const config = loadConfig(configPath);
  const countryCode = config.country.code;
  
  console.log(`🏳️  Building PWA for: ${config.country.name} (${countryCode})`);
  
  // Create output directory
  const output = path.join(outputDir, countryCode);
  if (!fs.existsSync(output)) {
    fs.mkdirSync(output, { recursive: true });
  }
  
  // Generate files
  console.log('📝 Generating index.html...');
  fs.writeFileSync(path.join(output, 'index.html'), generateIndexHTML(config));
  
  console.log('📝 Generating manifest.json...');
  fs.writeFileSync(path.join(output, 'manifest.json'), generateManifest(config));
  
  console.log('📝 Generating service worker...');
  fs.writeFileSync(path.join(output, 'sw.js'), generateServiceWorker(config));
  
  // Create icons directory
  const iconsDir = path.join(output, 'icons');
  if (!fs.existsSync(iconsDir)) {
    fs.mkdirSync(iconsDir);
  }
  console.log('📁 Icons directory created (add your icon files here)');
  
  console.log(`\n✅ Build complete!`);
  console.log(`📦 Output: ${output}`);
  console.log(`\n🚀 To deploy:`);
  console.log(`   1. Add icon files to ${path.join(output, 'icons')}`);
  console.log(`   2. Deploy the ${output} folder to any static host`);
  console.log(`   3. Test offline by opening in browser and disconnecting`);
  console.log(`\n💙 Built for ${config.country.name}. For WE. 🌍`);
}

// CLI
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.error('Usage: node build.js <country-config.json> [output-dir]');
    process.exit(1);
  }
  build(args[0], args[1]);
}

module.exports = { build };
