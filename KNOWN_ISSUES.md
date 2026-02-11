# Known Issues & Quick Fixes

This file documents non-obvious failure modes to save future debugging time.

## 1. "All agents failed" or API errors
- **Symptom:** The orchestrator reports a total failure, often with `AuthenticationError` or "Failed to get LLM response"
- **Cause:** The `ANTHROPIC_API_KEY` environment variable is not set in the shell session on VPS
- **Fix:** 
  ```bash
  export ANTHROPIC_API_KEY="sk-ant-api03-..."
  echo 'export ANTHROPIC_API_KEY="sk-ant-..."' >> ~/.bashrc
  source ~/.bashrc
  cd ~/Deliberate-AI-Ensemble
  pkill -f "streamlit.*8502"
  nohup streamlit run consensus_checker/app.py --server.port 8502 --server.address 0.0.0.0 > consensus_checker.log 2>&1 &
  ```

## 2. UI elements are invisible/unreadable
- **Symptom:** Streamlit UI has black-on-black text for buttons or expander headers
- **Cause:** Default Streamlit theme clashing with custom CSS, especially in dark mode
- **Fix:** Force-color CSS override was implemented. If this recurs, check the CSS injection logic in consensus_checker/app.py. (Ref: commits ae558a6, 9d384a7)

## 3. Rapid credit burn without progress
- **Symptom:** Anthropic billing shows high cost, but logs show few successful cycles
- **Cause:** The rate limiter logic was recording usage *after* the API call, so failed calls weren't being counted, leading to rapid retries and uncounted burns
- **Fix:** The logic was moved to correctly increment the limiter *before* the orchestrator.verify_claim() call. (Ref: commit 3b461d0)
- **Cost:** This bug burned ~$100 in 90 minutes during stress testing

## 4. Indentation errors on deployment
- **Symptom:** `IndentationError: unindent does not match any outer indentation level` on line 155 of app.py
- **Cause:** Inconsistent whitespace (tabs vs spaces) introduced during multi-file edits
- **Fix:** Corrected try block indentation to consistent 4-space alignment. (Ref: commit 9a12202)

## 5. KeyError: 'agreement_ratio' when verification fails
- **Symptom:** App crashes with KeyError when trying to display consensus metrics after all agents fail
- **Cause:** Frontend tried to render metrics from consensus["details"]["agreement_ratio"] even when consensus analysis returned ERROR state with no details
- **Fix:** Added defensive checks for is_error state and has_stats validation before rendering metrics section. (Ref: commit 58cbcef)

## 6. Anthropic API requires billing setup
- **Symptom:** 0 token usage despite API key being set correctly
- **Cause:** Evaluation plan requires payment method on file, even for free tier
- **Fix:** Add payment method in Anthropic Console > Billing. Typically need $5 minimum deposit.
- **Note:** Claude Pro subscription is separate from API access - they don't share billing

## VPS Deployment Commands

**Check if services are running:**
```bash
curl http://187.77.3.56:8501  # Operation Nightingale
curl http://187.77.3.56:8502  # WE Consensus Checker
ps aux | grep streamlit
```

**Restart Consensus Checker:**
```bash
cd ~/Deliberate-AI-Ensemble
git pull origin master
pkill -f "streamlit.*8502"
nohup streamlit run consensus_checker/app.py --server.port 8502 --server.address 0.0.0.0 > consensus_checker.log 2>&1 &
tail -f consensus_checker.log  # verify no errors
```

**Check logs for errors:**
```bash
tail -50 ~/Deliberate-AI-Ensemble/consensus_checker.log
```
