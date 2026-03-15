#!/usr/bin/env node

/**
 * WE4Free Config Validator
 * 
 * Validates country configuration files before build.
 * Ensures safe community contributions.
 * 
 * Usage:
 *   node validate.js config_canada.json
 *   node validate.js configs/*.json
 */

const fs = require('fs');
const path = require('path');

class ConfigValidator {
  constructor() {
    this.errors = [];
    this.warnings = [];
  }

  /**
   * Validate a config file
   * @param {string} configPath - Path to config JSON file
   * @returns {Object} - { valid: boolean, errors: [], warnings: [] }
   */
  validate(configPath) {
    this.errors = [];
    this.warnings = [];

    // Load config
    let config;
    try {
      const configData = fs.readFileSync(configPath, 'utf8');
      config = JSON.parse(configData);
    } catch (error) {
      this.errors.push(`Failed to load config: ${error.message}`);
      return this.getResult();
    }

    // Run validation checks
    this.validateRequired(config);
    this.validateCountry(config);
    this.validateEmergencyNumber(config);
    this.validateCrisisLines(config);
    this.validatePWASettings(config);
    this.validateURLs(config);

    return this.getResult();
  }

  /**
   * Check required top-level fields
   */
  validateRequired(config) {
    // Country object is required
    if (!config.country || typeof config.country !== 'object') {
      this.errors.push('Missing required field: country (must be object)');
      return;
    }
    
    // Country sub-fields
    const countryRequired = ['code', 'name', 'languages'];
    for (const field of countryRequired) {
      if (!config.country[field]) {
        this.errors.push(`Missing required field: country.${field}`);
      }
    }
    
    // Crisis lines required
    if (!config.crisis_lines) {
      this.errors.push('Missing required field: crisis_lines');
    } else if (config.crisis_lines === null) {
      this.errors.push('crisis_lines cannot be null');
    }
  }

  /**
   * Validate country object
   */
  validateCountry(config) {
    if (!config.country) return; // Already caught in validateRequired
    
    const country = config.country;

    // Country code: 2-3 uppercase letters (ISO 3166)
    if (country.code && !/^[A-Z]{2,3}$/.test(country.code)) {
      this.errors.push(`Invalid country.code '${country.code}' - must be 2-3 uppercase letters (ISO 3166)`);
    }

    // Country name: reasonable length
    if (country.name && (country.name.length < 2 || country.name.length > 100)) {
      this.warnings.push(`country.name '${country.name}' is unusually short/long`);
    }

    // Languages: must be array with at least one language
    if (country.languages) {
      if (!Array.isArray(country.languages)) {
        this.errors.push('country.languages must be an array');
      } else if (country.languages.length === 0) {
        this.errors.push('country.languages must contain at least one language code');
      } else {
        // Validate language codes (ISO 639-1 format)
        country.languages.forEach(lang => {
          if (!/^[a-z]{2}(-[A-Z]{2})?$/.test(lang)) {
            this.warnings.push(`Language code '${lang}' may not be valid ISO 639-1 format (e.g., 'en', 'fr-CA')`);
          }
        });

        // Check for duplicates
        const uniqueLangs = new Set(country.languages);
        if (uniqueLangs.size !== country.languages.length) {
          this.errors.push('country.languages contains duplicate language codes');
        }
      }
    }
  }

  /**
   * Validate emergency number
   */
  validateEmergencyNumber(config) {
    if (!config.country || !config.country.emergency_number) {
      this.warnings.push('No country.emergency_number provided (recommended for local emergency services)');
      return;
    }

    const num = config.country.emergency_number;
    
    // Must be string
    if (typeof num !== 'string') {
      this.errors.push(`country.emergency_number must be a string, got ${typeof num}`);
      return;
    }
    
    // Must not be empty
    if (num.trim() === '') {
      this.errors.push('country.emergency_number cannot be empty');
      return;
    }
    
    // Extract digits
    const digits = num.replace(/\D/g, '');
    
    // Must contain only digits/spaces/hyphens/parentheses
    if (!/^[\d\s\-()]+$/.test(num)) {
      this.errors.push(`country.emergency_number '${num}' contains invalid characters (only digits, spaces, hyphens, parentheses allowed)`);
    }
    
    // Must be 2-6 digits
    if (digits.length < 2) {
      this.errors.push(`country.emergency_number '${num}' too short (${digits.length} digits, minimum 2)`);
    }
    if (digits.length > 6) {
      this.errors.push(`country.emergency_number '${num}' too long (${digits.length} digits, maximum 6)`);
    }
    
    // Warn if not a common emergency number
    const knownEmergency = ['911', '999', '112', '000', '110', '119', '122'];
    if (!knownEmergency.includes(digits)) {
      this.warnings.push(`Emergency number '${digits}' is not a common international emergency number (911/999/112/000/110/119/122)`);
    }
  }

  /**
   * Validate crisis lines array
   */
  validateCrisisLines(config) {
    if (!Array.isArray(config.crisis_lines)) {
      this.errors.push('crisis_lines must be an array');
      return;
    }

    if (config.crisis_lines.length === 0) {
      this.errors.push('At least one crisis line is required');
      return;
    }

    const seenIds = new Set();
    const seenNames = new Set();

    config.crisis_lines.forEach((line, index) => {
      const lineNum = index + 1;
      const lineName = line.name || `line ${lineNum}`;

      // Check for duplicate id
      if (line.id) {
        if (seenIds.has(line.id)) {
          this.errors.push(`Crisis line ${lineNum}: Duplicate id '${line.id}'`);
        }
        seenIds.add(line.id);
      }

      // Required: name
      if (!line.name || typeof line.name !== 'string' || line.name.trim() === '') {
        this.errors.push(`Crisis line ${lineNum}: Missing or invalid 'name' (must be non-empty string)`);
      } else {
        // Warn on duplicate names
        if (seenNames.has(line.name)) {
          this.warnings.push(`Crisis line ${lineNum}: Duplicate name '${line.name}'`);
        }
        seenNames.add(line.name);
      }

      // Required: description
      if (!line.description || typeof line.description !== 'string' || line.description.trim() === '') {
        this.errors.push(`Crisis line ${lineNum} (${lineName}): Missing or invalid 'description'`);
      }

      // Required: at least one contact method
      const hasContact = line.phone || line.sms || line.chat || line.chat_url || line.email || line.website;
      if (!hasContact) {
        this.errors.push(`Crisis line ${lineNum} (${lineName}): Must have at least one contact method (phone/sms/chat/chat_url/email/website)`);
      }

      // Validate phone if provided
      if (line.phone) {
        this.validatePhone(line.phone, `Crisis line ${lineNum} (${lineName}) phone`, {requireMin: 7});
      }

      //Validate SMS if provided (can be short codes or keywords)
      if (line.sms) {
        // SMS can include keywords like "SPEAK to 9820466726" or be short codes like "988"
        if (typeof line.sms === 'string') {
          const digits = line.sms.replace(/\D/g, '');
          if (digits.length === 0) {
            this.errors.push(`Crisis line ${lineNum} (${lineName}) SMS: No phone number found in '${line.sms}'`);
          } else if (digits.length < 3) {
            this.errors.push(`Crisis line ${lineNum} (${lineName}) SMS: Phone number too short (${digits.length} digits)`);
          } else if (digits.length >= 3 && digits.length <= 6) {
            // Short codes are valid for SMS
            this.warnings.push(`Crisis line ${lineNum} (${lineName}) SMS: Short code '${line.sms}' (${digits.length} digits) - verify this is correct`);
          }
          // Otherwise accept it (can contain text or be longer number)
        } else {
          this.errors.push(`Crisis line ${lineNum} (${lineName}) SMS: Must be a string`);
        }
      }

      // Validate email if provided
      if (line.email && !this.isValidEmail(line.email)) {
        this.errors.push(`Crisis line ${lineNum} (${lineName}): Invalid email '${line.email}'`);
      }

      // Validate URLs
      if (line.website && !this.isValidURL(line.website)) {
        this.errors.push(`Crisis line ${lineNum} (${lineName}): Invalid website URL '${line.website}'`);
      }

      if (line.chat_url && !this.isValidURL(line.chat_url)) {
        this.errors.push(`Crisis line ${lineNum} (${lineName}): Invalid chat_url '${line.chat_url}'`);
      }

      if (line.chat && !this.isValidURL(line.chat)) {
        this.errors.push(`Crisis line ${lineNum} (${lineName}): Invalid chat URL '${line.chat}'`);
      }

      // Validate languages if provided
      if (line.languages) {
        if (!Array.isArray(line.languages)) {
          this.errors.push(`Crisis line ${lineNum} (${lineName}): 'languages' must be an array`);
        } else if (line.languages.length === 0) {
          this.warnings.push(`Crisis line ${lineNum} (${lineName}): 'languages' array is empty`);
        } else if (config.country && Array.isArray(config.country.languages)) {
          // Check that line languages are subset of country languages
          line.languages.forEach(lang => {
            if (!config.country.languages.includes(lang)) {
              this.warnings.push(`Crisis line ${lineNum} (${lineName}): Language '${lang}' not found in country.languages [${config.country.languages.join(', ')}]`);
            }
          });
        }
      } else {
        this.warnings.push(`Crisis line ${lineNum} (${lineName}): No 'languages' specified (recommended)`);
      }

      // Recommend hours/availability
      if (!line.hours && !line.availability) {
        this.warnings.push(`Crisis line ${lineNum} (${lineName}): Missing 'hours' or 'availability' (recommended to specify)`);
      }
    });
  }

  /**
   * Validate phone number format
   */
  validatePhone(phone, context, options = {}) {
    const {requireMin = 7} = options;
    
    if (typeof phone !== 'string') {
      this.errors.push(`${context}: Must be a string, got ${typeof phone}`);
      return;
    }

    // Must contain only digits, spaces, hyphens, parentheses, plus
    if (!/^[\d\s\-()+ ]+$/.test(phone)) {
      this.errors.push(`${context}: '${phone}' contains invalid characters`);
      return; // Don't continue if invalid format
    }

    // Extract digits
    const digits = phone.replace(/\D/g, '');
    
    // Special case: Emergency/short codes (3-6 digits) are valid
    if (digits.length >= 3 && digits.length <= 6) {
      // Warn but don't error on short codes (988, 111, 13 11 14, etc.)
      this.warnings.push(`${context}: Short code '${phone}' (${digits.length} digits) - verify this is correct`);
      return;
    }
    
    // Standard phone numbers: at least requireMin digits
    if (digits.length < requireMin && digits.length < 3) {
      this.errors.push(`${context}: '${phone}' too short (${digits.length} digits, minimum ${requireMin})`);
    }

    // Reasonable maximum
    if (digits.length > 15) {
      this.warnings.push(`${context}: '${phone}' seems long (${digits.length} digits)`);
    }
  }

  /**
   * Validate PWA settings if provided
   */
  validatePWASettings(config) {
    if (!config.pwa_settings) {
      this.warnings.push('pwa_settings not provided - defaults will be used');
      return;
    }

    const pwa = config.pwa_settings;

    // Validate theme color (hex format)
    if (pwa.theme_color && !/^#[0-9A-Fa-f]{6}$/.test(pwa.theme_color)) {
      this.errors.push(`Invalid pwa_settings.theme_color '${pwa.theme_color}' - must be hex format (#RRGGBB)`);
    }

    // Validate background color
    if (pwa.background_color && !/^#[0-9A-Fa-f]{6}$/.test(pwa.background_color)) {
      this.errors.push(`Invalid pwa_settings.background_color '${pwa.background_color}' - must be hex format (#RRGGBB)`);
    }

    // Validate display mode
    const validDisplay = ['standalone', 'fullscreen', 'minimal-ui', 'browser'];
    if (pwa.display && !validDisplay.includes(pwa.display)) {
      this.errors.push(`Invalid pwa_settings.display '${pwa.display}' - must be one of: ${validDisplay.join(', ')}`);
    }

    // Validate orientation
    const validOrientation = ['any', 'natural', 'landscape', 'portrait', 'portrait-primary', 'portrait-secondary', 'landscape-primary', 'landscape-secondary'];
    if (pwa.orientation && !validOrientation.includes(pwa.orientation)) {
      this.errors.push(`Invalid pwa_settings.orientation '${pwa.orientation}' - must be one of: ${validOrientation.join(', ')}`);
    }
  }

  /**
   * Validate URLs in config
   */
  validateURLs(config) {
    if (config.metadata) {
      if (config.metadata.site_url && !this.isValidURL(config.metadata.site_url)) {
        this.warnings.push(`metadata.site_url '${config.metadata.site_url}' may be invalid`);
      }
    }
  }

  /**
   * Check if email is valid format
   */
  isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }

  /**
   * Check if URL is valid format
   */
  isValidURL(url) {
    try {
      new URL(url);
      return true;
    } catch {
      return false;
    }
  }

  /**
   * Get validation result
   */
  getResult() {
    return {
      valid: this.errors.length === 0,
      errors: this.errors,
      warnings: this.warnings
    };
  }
}

/**
 * CLI Interface
 */
if (require.main === module) {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    console.log('Usage: node validate.js <config-file.json>');
    console.log('       node validate.js ../configs/*.json');
    process.exit(1);
  }

  let totalFiles = 0;
  let validFiles = 0;
  let invalidFiles = 0;

  // Process each config file
  args.forEach(configPath => {
    totalFiles++;
    
    const validator = new ConfigValidator();
    const result = validator.validate(configPath);
    
    const filename = path.basename(configPath);
    
    if (result.valid) {
      console.log(`✅ ${filename}: VALID`);
      validFiles++;
      
      if (result.warnings.length > 0) {
        result.warnings.forEach(warning => {
          console.log(`   ⚠️  ${warning}`);
        });
      }
    } else {
      console.log(`❌ ${filename}: INVALID`);
      invalidFiles++;
      
      result.errors.forEach(error => {
        console.log(`   ❌ ${error}`);
      });
      
      if (result.warnings.length > 0) {
        result.warnings.forEach(warning => {
          console.log(`   ⚠️  ${warning}`);
        });
      }
    }
    
    console.log('');
  });

  // Summary
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log(`📊 Summary: ${validFiles} valid, ${invalidFiles} invalid (${totalFiles} total)`);
  
  if (invalidFiles > 0) {
    console.log('❌ Validation failed - fix errors before building');
    process.exit(1);
  } else {
    console.log('✅ All configs valid!');
    process.exit(0);
  }
}

// Export for use as module
module.exports = ConfigValidator;
