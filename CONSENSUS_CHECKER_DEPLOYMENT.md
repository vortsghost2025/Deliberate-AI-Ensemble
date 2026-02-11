# WE Consensus Checker - Deployment Guide

**Date:** February 11, 2026  
**Status:** Ready for deployment  
**Port:** 8502  

---

## Pre-Deployment Checklist

### 1. Environment Setup

```powershell
# Ensure ANTHROPIC_API_KEY is set
$env:ANTHROPIC_API_KEY = "your-api-key-here"

# Verify it's set
echo $env:ANTHROPIC_API_KEY
```

### 2. Dependencies Check

```powershell
# Install required packages (if not already installed)
pip install streamlit anthropic
```

### 3. Test Locally First

```powershell
# From workspace root
cd C:\workspace

# Run locally on different port to test
streamlit run consensus_checker/app.py --server.port 8503
```

Open browser to `http://localhost:8503` and verify:
- ✅ Page loads
- ✅ Rate limiter shows stats
- ✅ Can enter claim
- ✅ Verification works (test with simple claim)
- ✅ All 3 agents return results
- ✅ Consensus analysis displays

### 4. Stop Test Instance

```powershell
# Kill the test process
# Use Ctrl+C in terminal where it's running
```

---

## VPS Deployment

### Option 1: Deploy Fresh (Recommended)

```bash
# SSH to VPS
ssh user@187.77.3.56

# Navigate to repo
cd /path/to/Deliberate-AI-Ensemble

# Pull latest code
git pull origin master

# Set API key (add to ~/.bashrc for persistence)
export ANTHROPIC_API_KEY="your-api-key-here"

# Stop any existing process on 8502
pkill -f "streamlit.*8502"

# Deploy with nohup
nohup streamlit run consensus_checker/app.py --server.port 8502 --server.address 0.0.0.0 > consensus_checker.log 2>&1 &

# Verify it's running
ps aux | grep streamlit

# Check logs
tail -f consensus_checker.log
```

### Option 2: Quick Check Current State

```bash
# SSH to VPS
ssh user@187.77.3.56

# Check what's running on 8502
lsof -i :8502

# If nothing, deploy fresh (see Option 1)
# If something is running, check what it is:
ps aux | grep streamlit
```

---

## Post-Deployment Verification

### 1. Check App is Live

```bash
# From VPS
curl http://localhost:8502

# Should return HTML content
```

### 2. Test from External Browser

Open: `http://187.77.3.56:8502`

Verify:
- ✅ Page loads completely
- ✅ Disclaimers visible
- ✅ Resource notice displays with current stats
- ✅ Can submit test claim
- ✅ Rate limiting works (try 3-4 claims in succession)

### 3. Monitor Logs

```bash
# Watch for errors
tail -f consensus_checker.log

# Or if using nohup.out
tail -f nohup.out
```

### 4. Check Rate Limiter Data

```bash
# View rate limit state
cat consensus_checker/rate_limits.json
```

Should show:
```json
{
  "checks": [list of timestamps],
  "total_checks": number
}
```

---

## Troubleshooting

### Issue: Port 8502 already in use

```bash
# Find process using port
lsof -i :8502

# Kill it
kill -9 <PID>

# Or kill all streamlit
pkill -9 streamlit

# Redeploy
```

### Issue: API key not recognized

```bash
# Verify key is set
echo $ANTHROPIC_API_KEY

# If empty, set it:
export ANTHROPIC_API_KEY="your-key-here"

# Restart app
pkill -f "streamlit.*8502"
nohup streamlit run consensus_checker/app.py --server.port 8502 --server.address 0.0.0.0 &
```

### Issue: Rate limiter file errors

```bash
# Check if file exists and is writable
ls -la consensus_checker/rate_limits.json

# If missing, it will be created automatically
# If permission issue:
chmod 644 consensus_checker/rate_limits.json
```

### Issue: App crashes on first verification

Check logs:
```bash
tail -100 consensus_checker.log
```

Common causes:
- API key invalid/expired
- Network connectivity to Anthropic API
- JSON parsing errors in agent responses

---

## Monitoring

### Check App Status

```bash
# Is it running?
ps aux | grep "consensus_checker"

# Check port
netstat -tulpn | grep 8502
```

### Monitor Usage

```bash
# Watch rate limit stats
watch -n 10 'cat consensus_checker/rate_limits.json | jq .'
```

### Check Resource Usage

```bash
# CPU/Memory
top -p $(pgrep -f consensus_checker)
```

---

## Rollback Plan

If deployment fails:

```bash
# Kill new deployment
pkill -f "streamlit.*8502"

# Restore from previous commit (if needed)
git log --oneline -5  # Find previous commit
git checkout <previous-commit-hash>

# Redeploy old version
nohup streamlit run consensus_checker/app.py --server.port 8502 --server.address 0.0.0.0 &
```

---

## Launch Checklist

Before announcing:

- [ ] App deployed to http://187.77.3.56:8502
- [ ] Test verification completes successfully
- [ ] Rate limiting works (test 3-4 claims)
- [ ] All 3 agents return results
- [ ] Consensus analysis displays correctly
- [ ] Logs show no errors
- [ ] Resource notice displays correctly
- [ ] Email link works: ai@deliberateensemble.works
- [ ] GitHub link works
- [ ] Footer links functional

---

## Launch Announcement (X Post)

Ready to deploy at 6 AM Feb 12:

```
The entire AI industry is selling 16 different fire extinguishers.

I figured out how to build houses that don't catch fire.

Example: Got tired of biased fact-checkers. Built this in 4 hours.

WE Consensus Checker
→ 3 independent AI reviewers
→ No agenda, no edits, no logs
→ 100% free

http://187.77.3.56:8502

Disagreement between agents isn't a bug—it's the most important signal we can give you.

Don't trust me. Verify consensus yourself.

Full breakdown: [GitHub repo link]
```

---

**Built Following Nightingale Pattern:**
- Idea to deployment: 4 hours
- Constitutional principles: embedded
- Privacy by omission: no data storage
- Restraint as feature: rate limiting
- For US: always

🚀
