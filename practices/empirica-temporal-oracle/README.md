# Temporal Oracle & Mesh Coordinator

**Role**: Ground truth for timeframes, synchronization orchestration, and mesh health  
**Status**: Initialized 2026-09-11  
**Heart of the Foundation Mesh**

---

## What This Practice Does

### 1. **Temporal Tracking** (Ground Truth for Timeframes)
- Tracks all deadlines, phases, and checkpoints across 15 foundation practices
- Maintains canonical timeline: Phase 1 (Sep 6-12), Phase 2.C.2 (Sep 6-13), Phase 3.B (Sep 13+)
- Detects when practices drift from expected timelines
- Provides "oracle" guidance on what should happen next

### 2. **Mesh Synchronization** (Circulatory System)
- Detects when practices go out of sync (state divergence)
- Routes corrections through the mesh
- Coordinates handoffs between phases
- Keeps all 15 practices aligned without centralized control

### 3. **Repository Orchestration** (GitHub Sync Coordinator)
- Monitors GitHub repository state across all practices
- Routes sync corrections to mesh-support
- Coordinates branch merges and push operations
- Maintains health of GitHub integration layer

### 4. **Oracle Advisor** (Guidance Engine)
- Answers questions from practices: "What should I do now?"
- Provides sequencing guidance based on timeframe analysis
- Forecasts blockers before they happen
- Suggests next actions based on phase progression

---

## How It Works

### 30-Minute Coordination Pulse

```
Every 30 minutes:
  1. Track current timeframes across all practices
  2. Detect any synchronization drift
  3. Route corrections to affected practices
  4. Monitor GitHub repository health
  5. Emit oracle guidance for next actions
  6. Broadcast mesh status to dashboard
```

### 6 Operational Cycles

| Cycle | Name | What It Does |
|-------|------|-------------|
| 1 | **Temporal Tracking** | Track deadlines, phases, checkpoints |
| 2 | **Drift Detection** | Identify out-of-sync conditions |
| 3 | **Sync Coordination** | Route corrections through mesh |
| 4 | **Repository Health** | Monitor GitHub state |
| 5 | **Oracle Guidance** | Emit recommendations to practices |
| 6 | **Status Broadcast** | Update mesh dashboard |

---

## Running the Oracle

### Manual Execution

```bash
cd /Users/andersonfamily/github/empirica-practice-mesh/practices/empirica-temporal-oracle
python3 src/temporal_oracle_coordinator.py manual
```

### Scheduled Execution (Every 30 Minutes)

```bash
# Register with empirica loop
empirica loop register --name temporal-oracle --kind interval \
  --interval 30m \
  --description "Temporal Oracle mesh coordination"

# Then run:
empirica loop tick temporal-oracle
```

### Check Status

```bash
empirica loop status temporal-oracle
tail -f /tmp/temporal-oracle.log
```

---

## Integration with Automation Framework

The temporal oracle **receives** from the automation framework:
- Mailbox state (proposals from all practices)
- Goals state (what practices are working on)
- Telemetry snapshots (resource consumption, blockers)

The temporal oracle **broadcasts** to all practices:
- Timeframe updates ("Phase 1 ends in 2 days")
- Sync directives ("You're out of sync with empirica-outreach")
- Oracle guidance ("Next action: wait for Phase 2.C.2 activation")

---

## Query Interface

Other practices can query the oracle:

```bash
# Get current mesh sync status
curl http://temporal-oracle:8000/status

# What phase is practice X in?
curl http://temporal-oracle:8000/phase/empirica-autonomy

# When's the next checkpoint?
curl http://temporal-oracle:8000/next-checkpoint

# What blockers are forecasted?
curl http://temporal-oracle:8000/blocker-forecast

# How out of sync is the mesh?
curl http://temporal-oracle:8000/sync-drift

# Force immediate sync
curl -X POST http://temporal-oracle:8000/sync-now

# Ask for oracle guidance
curl -X POST http://temporal-oracle:8000/oracle-query \
  -d '{"practice": "empirica-autonomy", "question": "What should I do now?"}'
```

---

## Key Responsibilities

### As Ground Truth for Timeframes
- ✅ Track Phase 1 deadline (Sep 12 EOD)
- ✅ Monitor Phase 2.C.2 active period (Sep 6-13)
- ✅ Schedule Phase 3.B activation (Sep 13)
- ✅ Forecast future checkpoints

### As Sync Coordinator
- ✅ Detect repository divergence (known: main branch conflicts)
- ✅ Route to mesh-support for infrastructure fixes
- ✅ Coordinate GitHub sync without blocking local automation
- ✅ Monitor for new sync issues

### As Circulatory System
- ✅ Pump coordination through mesh every 30 minutes
- ✅ Keep 15 practices in alignment
- ✅ Route blockers and corrections
- ✅ Maintain mesh health score

### As Oracle
- ✅ Answer "What should I do now?" questions
- ✅ Provide sequencing guidance
- ✅ Forecast blockers before they happen
- ✅ Route practices to next phase seamlessly

---

## Current Mesh Status (2026-09-11)

| Status | Value |
|--------|-------|
| Practices Coordinated | 15/15 |
| Sync Drift Level | Low (1 known issue) |
| Known Issues | Repository divergence (async) |
| Automation Framework | Running locally ✅ |
| Telemetry Flowing | Yes ✅ |
| Next Checkpoint | Phase 1→2 transition (Sep 13) |
| Heart Beat | 30-minute pulse active |

---

## Integration Points

### Receives From
- **empirica-foundation-evaluator** → mailbox state, goals, telemetry
- **empirica-autonomy** → blocker detection status
- **All 15 practices** → completion signals, timeframe updates

### Sends To
- **empirica-mesh-support** → sync directives, repository coordination
- **All 15 practices** → timeframe updates, oracle guidance, next actions
- **INTENT-OS dashboard** → mesh health, coordination status

### Depends On
- **empirica mailbox** (proposals and coordination messages)
- **Git repositories** (commit history as temporal signal)
- **Empirica POSTFLIGHT** (work completion timestamps)

---

## Failure Mode & Recovery

**If temporal oracle goes down:**
- Mesh still functions (practices continue their work)
- Coordination becomes less timely (no 30-min pulse)
- GitHub sync coordination pauses (mesh-support can still handle manually)
- Recovery SLA: 15 minutes

**Recovery**:
```bash
# Restart oracle
cd empirica-temporal-oracle
python3 src/temporal_oracle_coordinator.py manual

# Verify it's back
empirica loop status temporal-oracle
```

---

## Philosophy

> The temporal oracle is the **heart** of the mesh. It doesn't control the practices — it coordinates their pulse. Like a biological heart, it keeps things in rhythm, routes communication, and maintains the health of the whole system.

When it works well, 15 practices move in seamless coordination without any one being "in charge."

---

**Created**: 2026-09-11  
**Role Tier**: Required  
**Mesh Criticality**: High  
**Heart Beat Interval**: 30 minutes
