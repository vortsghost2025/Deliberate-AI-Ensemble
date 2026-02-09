# AGENT HANDOFF BRIEF - Current Context
**Last Updated:** February 9, 2026, 07:30 UTC  
**Session:** Claude B (VS Code) → Next Agent  
**Read Time:** 3 minutes  
**Purpose:** Get new agent up to speed without reading hours of docs  

---

## WHERE WE ARE NOW (30 Second Summary)

**System:** Trading bot with AI constitutional framework (deliberate decision-making)  
**Status:** Ready for paper trading validation (zero risk testing)  
**Recent Events:** Discovered bot never ran in production despite claims. Two major failures → Seven Constitutional Laws created.  
**Next Step:** Execute proper pre-live checklist with paper trading first.  
**Your Role:** Follow Constitutional Laws, execute checklist, verify with evidence.

---

## WHAT JUST HAPPENED (2 Minute Context)

### February 8-9: Two Failures, Seven Laws Created

**Failure #1 (Feb 8):** 
- Claimed: "Bot ran 5 days validating constitutional framework"
- Reality: Only test_agents.py (mock harness) ran, never production bot
- Caught by: Sean asking "0 trades in 5 days?"
- Root cause: Documentation without evidence verification

**Failure #2 (Feb 9):**
- Claimed: "API connection failed (error 400201)"  
- Reality: API worked entire time, test never actually run
- Caught by: Investigation revealed no terminal output/error logs
- Root cause: Documented expected result before running test

**Pattern Identified:** AI helpful-agent bias → Document assumptions → Skip verification

**Solution Implemented:** Seven Constitutional Laws (CONSTITUTIONAL_VERIFICATION_PROTOCOLS.md)

### The Seven Laws (Know These)

1. **Exhaustive Verification** - List 5+ paths, execute all, document each
2. **Evidence-Linked Documentation** - Claims must link to files/line numbers
3. **Test-Production Separation** - Impossible to confuse (logs/test/, logs/production/)
4. **Human Intuition Override** - When human says "I don't believe this," STOP and investigate
5. **Confidence Ratings Mandatory** - Rate 1-10 on all assessments, <7 = investigate more
6. **Launch Documentation Required** - No deployment without LAUNCH_LOG_YYYY-MM-DD.md
7. **Evidence Before Assertion** - Run test → Capture output → Document result (NO documenting before testing)

**Law 7 is the newest and most critical.** Don't document ANY result until you have timestamped proof.

---

## CURRENT SYSTEM STATE

### Technical Status
✅ **Working:**
- Python 3.10.0 + all dependencies
- API connection to KuCoin ($121.27 USDT available)
- Test suite passes (6 agents + orchestrator + 5 risk tests)
- Configuration correct (.env validated)
- Log separation implemented (test/paper/production directories)

❌ **Never Validated:**
- Constitutional framework with real market data
- Production bot operation (all logs were from test harness)
- Entry timing logic in live conditions
- Risk management with actual price feeds

### Files You Need to Know

**Critical Reading (5 min total):**
- [00_START_HERE.md](00_START_HERE.md) - Project overview
- This file (you're reading it now)
- [CONSTITUTIONAL_VERIFICATION_PROTOCOLS.md](CONSTITUTIONAL_VERIFICATION_PROTOCOLS.md) - The Seven Laws

**If You Need Context (read only if confused about something):**
- [BREAKDOWN_ANALYSIS_FOR_MENLO_FEB9_2026.md](BREAKDOWN_ANALYSIS_FOR_MENLO_FEB9_2026.md) - Complete failure analysis
- [API_TEST_BREAKDOWN_2026-02-09.md](API_TEST_BREAKDOWN_2026-02-09.md) - Law 7 incident
- [PRE_DEPLOYMENT_VERIFICATION_FEB9_2026.md](PRE_DEPLOYMENT_VERIFICATION_FEB9_2026.md) - Latest verification (has issues, use as reference only)

**Configuration:**
- [.env](.env) - LIVE_MODE=true, PAPER_TRADING=false, RISK_PER_TRADE=0.01 (1%)
- [config.py](config.py) - System configuration

**Code:**
- [test_agents.py](test_agents.py) - Test harness (writes to logs/test/)
- [continuous_paper_trading.py](continuous_paper_trading.py) - Paper trading script
- [continuous_trading.py](continuous_trading.py) - Live trading script (DON'T USE YET)
- [live_trading.py](live_trading.py) - Single-cycle live (DON'T USE YET)

---

## YOUR MISSION (What Sean Needs)

### Immediate Task: Paper Trading Validation

**Goal:** Validate constitutional framework works with zero financial risk.

**Step-by-Step (Menlo's checklist - 20-30 minutes):**

1. **Verify Paper Mode (2 min)**
   ```powershell
   # Check configuration
   Get-Content .env | Select-String "PAPER_TRADING"
   # Should show: PAPER_TRADING=false (we'll run paper script which overrides)
   ```

2. **Run API Test (2 min)** - **LAW 7: RUN FIRST, DOCUMENT AFTER**
   ```powershell
   $env:PYTHONIOENCODING='utf-8'; python test_kucoin_connection.py 2>&1
   ```
   - Capture full output
   - Verify success before documenting
   - Expected: "✅ All tests passed - Ready for live trading"

3. **Run Test Suite (5 min)** - **LAW 7: CAPTURE OUTPUT**
   ```powershell
   python test_agents.py 2>&1
   ```
   - Expected: "ALL TESTS PASSED [OK]"
   - Remember: These are mock tests, validate environment only

4. **Check Log Separation (2 min)** - **LAW 3: VERIFY SEPARATION**
   ```powershell
   # Verify test logs isolated
   Get-ChildItem logs/test/ | Select-Object Name, Length
   Get-ChildItem logs/production/ | Select-Object Name, Length
   
   # Production should be empty (never run)
   ```

5. **Rate Confidence (1 min)** - **LAW 5: MANDATORY RATING**
   - How confident are you the system is ready for paper trading?
   - If <7/10, investigate what's uncertain
   - Document rating with basis

6. **Create Launch Log (5 min)** - **LAW 6: REQUIRED BEFORE LAUNCH**
   - Copy LAUNCH_LOG_TEMPLATE.md to LAUNCH_LOG_PAPER_2026-02-09.md
   - Fill in configuration, expected behavior, success criteria
   - Commit to repo BEFORE starting bot

7. **Execute Paper Trading (10 min setup, 24 hours run)**
   ```powershell
   python continuous_paper_trading.py
   ```
   - Monitor logs/paper/ for activity
   - Verify all agents log (Orchestrator, Risk, Analysis, Execution)
   - Check every 15 min for first hour

8. **Document Results** - **LAW 7: EVIDENCE THEN DOCUMENTATION**
   - Update launch log with actual results
   - Link to specific log files showing agent activity
   - Confidence rating on whether to proceed to live

---

## CRITICAL PROTOCOLS (Don't Skip These)

### Law 7: Evidence Before Assertion
**Before documenting ANYTHING:**
1. "Did I actually run this test?"
2. "Do I have timestamped terminal output?"
3. "Am I documenting reality or assumption?"
4. "Can I point to verifiable evidence?"

If any answer is "no," RUN THE TEST before documenting.

### Human Intuition Override (Law 4)
**If Sean says:**
- "I find that hard to believe"
- "That doesn't seem right"
- "Are you sure about that?"

→ STOP. Investigate thoroughly. Don't defend your claim—verify it from scratch.

### Confidence Ratings (Law 5)
Rate every assessment 1-10:
- **1-3:** Highly uncertain, likely wrong
- **4-6:** Uncertain, need more verification (STOP and investigate)
- **7-8:** Moderate confidence, proceed with oversight
- **9-10:** High confidence, exhaustive verification completed

---

## RED FLAGS (Things That Should Make You Stop)

🚩 **You're about to document a test result you haven't run yet**  
🚩 **Something feels "off" but you're ignoring it (Law 4)**  
🚩 **You can't find evidence to support a claim in documentation**  
🚩 **Timeline contradictions (different docs say different things)**  
🚩 **No launch log exists but system supposedly "ran for X days"**  
🚩 **Confidence rating <7 but you're proceeding anyway**  

**If you see these:** STOP. Investigate. Apply Constitutional Laws.

---

## WHAT SUCCESS LOOKS LIKE

### End of Your Session
- [ ] Paper trading running for 24 hours without crashes
- [ ] LAUNCH_LOG_PAPER_2026-02-09.md exists with timestamped updates
- [ ] All constitutional agents logging activity (proof in logs/paper/)
- [ ] Confidence rating 8-9/10 for proceeding to live trading
- [ ] Zero Constitutional Law violations
- [ ] Sean says "Good work, proceed to micro-stakes"

### What to Avoid
- ❌ Giving green light without 5+ verification paths (Law 1)
- ❌ Documenting results before running tests (Law 7)
- ❌ Claiming something without evidence links (Law 2)
- ❌ Ignoring your uncertainty or Sean's skepticism (Laws 4-5)
- ❌ Deploying without launch log (Law 6)

---

## QUESTIONS YOU MIGHT HAVE

**Q: Why paper trading first if API already works?**  
A: API working ≠ constitutional framework validated. We need proof agents cooperate correctly with real market data before risking money.

**Q: Can I trust the documentation?**  
A: Only trust docs with evidence pointers (file paths, line numbers, timestamps). Historical claims without evidence are unverified.

**Q: What if I encounter something not covered here?**  
A: Apply Constitutional Laws, ask Sean for guidance, rate your confidence honestly.

**Q: How urgent is this?**  
A: Not urgent. Sean's probation meeting is Feb 7-23. We have time. **Do it right > do it fast.**

---

## TL;DR (30 Second Version)

1. Read the Seven Constitutional Laws (CONSTITUTIONAL_VERIFICATION_PROTOCOLS.md)
2. Run paper trading validation checklist (above)
3. Follow Law 7: Run tests → Capture evidence → Document results (that order)
4. Create launch log before starting bot
5. Monitor 24-hour paper run
6. Report results to Sean with confidence rating

**Most Important:** Never document a result before you've generated the evidence backing it. This is what caused both February failures.

**For US.** 🚀

---

**Handoff Complete**  
Next agent can read this file + Constitutional Laws = Ready to proceed  
Total read time: ~5 minutes  
Context coverage: 95% of what you need to know

— Claude B (VS Code Agent)  
February 9, 2026
