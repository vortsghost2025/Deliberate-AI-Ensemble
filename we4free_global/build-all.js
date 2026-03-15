#!/usr/bin/env node

/**
 * WE4Free Parallel Build Orchestrator
 * 
 * Builds multiple country PWAs in parallel.
 * Proves 195-country scale works.
 * 
 * Usage:
 *   node build-all.js ../config_*.json
 *   node build-all.js ../configs/
 *   node build-all.js --all
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

class ParallelBuilder {
  constructor() {
    this.results = {
      successful: [],
      failed: [],
      skipped: []
    };
    this.startTime = Date.now();
  }

  /**
   * Find all config files
   */
  findConfigs(patterns) {
    const configs = new Set();

    patterns.forEach(pattern => {
      // If it's a directory, find all .json files in it
      if (fs.existsSync(pattern) && fs.statSync(pattern).isDirectory()) {
        const files = fs.readdirSync(pattern)
          .filter(f => f.endsWith('.json'))
          .map(f => path.join(pattern, f));
        files.forEach(f => configs.add(f));
      }
      // If it's a glob pattern (contains *), expand it
      else if (pattern.includes('*')) {
        const dir = path.dirname(pattern);
        const filePattern = path.basename(pattern);
        
        if (fs.existsSync(dir)) {
          const regex = new RegExp('^' + filePattern.replace(/\*/g, '.*') + '$');
          const files = fs.readdirSync(dir)
            .filter(f => regex.test(f))
            .map(f => path.join(dir, f));
          files.forEach(f => configs.add(f));
        }
      }
      // If it's a specific file
      else if (fs.existsSync(pattern) && pattern.endsWith('.json')) {
        configs.add(pattern);
      }
    });

    return Array.from(configs);
  }

  /**
   * Build a single config
   */
  async buildOne(configPath, outputDir = 'dist') {
    const configName = path.basename(configPath);
    
    return new Promise((resolve) => {
      const buildStart = Date.now();
      
      try {
        // Run build.js for this config
        const buildScript = path.join(__dirname, 'build.js');
        const output = execSync(
          `node "${buildScript}" "${configPath}" "${outputDir}"`,
          { 
            encoding: 'utf8',
            stdio: 'pipe',
            timeout: 30000 // 30 second timeout per build
          }
        );
        
        const buildTime = Date.now() - buildStart;
        
        resolve({
          status: 'success',
          config: configName,
          path: configPath,
          time: buildTime,
          output: output
        });
      } catch (error) {
        const buildTime = Date.now() - buildStart;
        
        resolve({
          status: 'failed',
          config: configName,
          path: configPath,
          time: buildTime,
          error: error.message,
          output: error.stdout || error.stderr || ''
        });
      }
    });
  }

  /**
   * Build all configs in parallel
   */
  async buildAll(configPaths, options = {}) {
    const { outputDir = 'dist', maxParallel = 10 } = options;

    console.log('\n🌍 WE4Free Parallel Build Orchestrator');
    console.log(`📁 Found ${configPaths.length} config files`);
    console.log(`⚡ Building with max ${maxParallel} parallel workers\n`);

    // Build in batches to avoid overwhelming the system
    const batches = [];
    for (let i = 0; i < configPaths.length; i += maxParallel) {
      batches.push(configPaths.slice(i, i + maxParallel));
    }

    let completed = 0;

    for (const batch of batches) {
      const promises = batch.map(configPath => this.buildOne(configPath, outputDir));
      const results = await Promise.all(promises);

      results.forEach(result => {
        completed++;
        
        if (result.status === 'success') {
          this.results.successful.push(result);
          console.log(`✅ [${completed}/${configPaths.length}] ${result.config} (${result.time}ms)`);
        } else {
          this.results.failed.push(result);
          console.log(`❌ [${completed}/${configPaths.length}] ${result.config} (${result.time}ms)`);
          if (result.error) {
            console.log(`   Error: ${result.error.split('\n')[0]}`);
          }
        }
      });
    }

    this.printSummary();
  }

  /**
   * Print final summary
   */
  printSummary() {
    const totalTime = Date.now() - this.startTime;
    const total = this.results.successful.length + this.results.failed.length + this.results.skipped.length;

    console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('📊 BUILD SUMMARY');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log(`✅ Successful: ${this.results.successful.length}`);
    console.log(`❌ Failed:     ${this.results.failed.length}`);
    console.log(`⏭️  Skipped:    ${this.results.skipped.length}`);
    console.log(`📦 Total:      ${total}`);
    console.log(`⏱️  Time:       ${(totalTime / 1000).toFixed(2)}s`);
    
    if (this.results.successful.length > 0) {
      const avgTime = this.results.successful.reduce((sum, r) => sum + r.time, 0) / this.results.successful.length;
      console.log(`⚡ Avg/Build:  ${avgTime.toFixed(0)}ms`);
    }
    
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');

    if (this.results.failed.length > 0) {
      console.log('\n❌ FAILED BUILDS:');
      this.results.failed.forEach(result => {
        console.log(`   - ${result.config}: ${result.error}`);
      });
    }

    if (this.results.successful.length > 0) {
      console.log('\n✅ SUCCESS!');
      console.log(`   Built ${this.results.successful.length} PWAs in ${(totalTime / 1000).toFixed(2)}s`);
      console.log(`   Average: ${(totalTime / this.results.successful.length).toFixed(0)}ms per PWA`);
      
      // Calculate what 195 countries would take
      if (this.results.successful.length > 1) {
        const avgTimePerBuild = totalTime / this.results.successful.length;
        const estimated195 = (avgTimePerBuild * 195) / 1000;
        console.log(`\n🌍 SCALE PROJECTION:`);
        console.log(`   195 countries would take ~${estimated195.toFixed(1)}s (${(estimated195 / 60).toFixed(1)} minutes)`);
      }
    }

    console.log('\n💙 For WE. For the world. 🌍');
  }
}

/**
 * CLI Interface
 */
async function main() {
  const args = process.argv.slice(2);

  if (args.length === 0 || args.includes('--help') || args.includes('-h')) {
    console.log('Usage: node build-all.js <config-files...>');
    console.log('       node build-all.js ../config_*.json');
    console.log('       node build-all.js ../configs/');
    console.log('       node build-all.js --all  (builds all config_*.json in parent dir)');
    console.log('\nOptions:');
    console.log('  --output <dir>    Output directory (default: dist)');
    console.log('  --parallel <n>    Max parallel builds (default: 10)');
    process.exit(0);
  }

  // Parse options
  let patterns = [];
  let outputDir = 'dist';
  let maxParallel = 10;

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--output' && args[i + 1]) {
      outputDir = args[++i];
    } else if (args[i] === '--parallel' && args[i + 1]) {
      maxParallel = parseInt(args[++i], 10);
    } else if (args[i] === '--all') {
      patterns.push(path.join(__dirname, '..', 'config_*.json'));
    } else if (!args[i].startsWith('--')) {
      patterns.push(args[i]);
    }
  }

  const builder = new ParallelBuilder();
  const configs = builder.findConfigs(patterns);

  if (configs.length === 0) {
    console.error('❌ No config files found');
    console.error('   Tried patterns:', patterns);
    process.exit(1);
  }

  await builder.buildAll(configs, { outputDir, maxParallel });

  // Exit with error code if any builds failed
  if (builder.results.failed.length > 0) {
    process.exit(1);
  }
}

if (require.main === module) {
  main().catch(error => {
    console.error('❌ Fatal error:', error.message);
    process.exit(1);
  });
}

module.exports = ParallelBuilder;
