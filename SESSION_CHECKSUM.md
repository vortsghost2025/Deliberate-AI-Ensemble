# Session Checksum (Quick Verify)

Use this before any state-changing action (git push, file writes, deployments).

1. Re-read AGENT_COORDINATION/SHARED_TASK_QUEUE.md.
2. Confirm the "Last Updated" timestamp matches your last known state.
3. Re-read AGENT_COORDINATION/COORDINATION_LESSONS.md.
4. Run `python checksum_guard.py` and record the checksum in your update.
5. If anything is unexpected, STOP and ask for human confirmation.
6. Add the checksum to task/status updates in the **Checksum:** field.

This guards against silent agent swaps or partial context resets.
