#!/usr/bin/env node

/**
 * WE4Free Global - Deployment Script
 * 
 * Deploys a country PWA to GitHub Pages or custom domain
 * Usage: node deploy.js <country-code> [options]
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

function deploy(countryCode, options = {}) {
  const distPath = path.join(__dirname, 'dist', countryCode.toUpperCase());
  
  console.log(`🚀 WE4Free Global Deployment`);
  console.log(`📦 Country: ${countryCode.toUpperCase()}`);
  console.log(`📁 Source: ${distPath}`);
  
  // Verify dist folder exists
  if (!fs.existsSync(distPath)) {
    console.error(`❌ Error: ${distPath} does not exist. Run build first.`);
    process.exit(1);
  }
  
  // Check for GitHub Pages deployment
  if (options.githubPages) {
    deployToGitHubPages(distPath, countryCode, options);
  } else {
    console.log('\n📋 Manual deployment steps:');
    console.log(`\n1. Copy ${distPath} to your web server`);
    console.log(`2. Configure your domain to point to the folder`);
    console.log(`3. Ensure HTTPS is enabled (required for PWA)`);
    console.log(`4. Test offline functionality\n`);
  }
}

function deployToGitHubPages(distPath, countryCode, options) {
  console.log('\n🌐 Deploying to GitHub Pages...');
  
  const deployBranch = options.branch || `gh-pages-${countryCode.toLowerCase()}`;
  const repoPath = options.repo || process.cwd();
  
  try {
    // Create deploy directory
    const deployDir = path.join(__dirname, 'temp-deploy');
    if (fs.existsSync(deployDir)) {
      fs.rmSync(deployDir, { recursive: true });
    }
    fs.mkdirSync(deployDir, { recursive: true });
    
    // Copy files
    console.log(`📂 Copying files...`);
    execSync(`xcopy "${distPath}\\*" "${deployDir}\\" /E /I /Y`, { stdio: 'inherit' });
    
    // Initialize git in deploy directory
    process.chdir(deployDir);
    console.log(`🔧 Initializing Git...`);
    execSync('git init', { stdio: 'inherit' });
    execSync('git add -A', { stdio: 'inherit' });
    execSync(`git commit -m "Deploy ${countryCode} PWA"`, { stdio: 'inherit' });
    
    // Push to GitHub Pages branch
    console.log(`⬆️  Pushing to ${deployBranch}...`);
    const remote = options.remote || execSync('git remote get-url origin', { cwd: repoPath }).toString().trim();
    execSync(`git remote add origin ${remote}`, { stdio: 'inherit' });
    execSync(`git branch -M ${deployBranch}`, { stdio: 'inherit' });
    execSync(`git push -f origin ${deployBranch}`, { stdio: 'inherit' });
    
    // Cleanup
    process.chdir(__dirname);
    fs.rmSync(deployDir, { recursive: true });
    
    console.log(`\n✅ Deployed successfully!`);
    console.log(`\n🔗 Your PWA should be available at:`);
    console.log(`   https://your-username.github.io/your-repo/${countryCode.toLowerCase()}`);
    console.log(`\n📋 Next steps:`);
    console.log(`   1. Enable GitHub Pages in repository settings`);
    console.log(`   2. Select the ${deployBranch} branch`);
    console.log(`   3. Wait 1-2 minutes for deployment`);
    console.log(`   4. Visit your URL and test offline`);
    
  } catch (error) {
    console.error(`❌ Deployment failed: ${error.message}`);
    process.exit(1);
  }
}

// CLI
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.log('Usage: node deploy.js <country-code> [--github-pages] [--branch=name] [--repo=path]');
    console.log('\nExamples:');
    console.log('  node deploy.js CA                     # Show manual deployment instructions');
    console.log('  node deploy.js CA --github-pages      # Deploy to GitHub Pages');
    console.log('  node deploy.js US --github-pages --branch=main  # Deploy to specific branch');
    process.exit(1);
  }
  
  const countryCode = args[0];
  const options = {
    githubPages: args.includes('--github-pages'),
    branch: args.find(a => a.startsWith('--branch='))?.split('=')[1],
    repo: args.find(a => a.startsWith('--repo='))?.split('=')[1],
    remote: args.find(a => a.startsWith('--remote='))?.split('=')[1]
  };
  
  deploy(countryCode, options);
}

module.exports = { deploy };
