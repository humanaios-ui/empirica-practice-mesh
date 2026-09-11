# Quick Reference: Entity Sync Pipeline

**For:** empirica-foundation-evaluator seat  
**Purpose:** Fast lookup for common tasks, decisions, and debugging  
**Updated:** 2026-09-11

---

## At a Glance

| Metric | Value | Status |
|--------|-------|--------|
| Practices Discovered | 17 | ✅ |
| Projects Synced | 17 | ✅ |
| Contacts Found | 2 | ✅ |
| Relationships Established | 0 | 🟡 (pending owner_contact_id) |
| Validation Checks | 4/4 passing | ✅ |
| Last Sync | 2026-09-11 19:16:38 UTC | ✅ |
| Pipeline Status | OPERATIONAL | ✅ |

---

## Common Commands

### Run Sync Now
```bash
cd /home/user/empirica-practice-mesh
python3 scripts/sync_entity_registry.py
```

### Check Latest Results
```bash
tail -50 .empirica/sync.log
```

### Search for Errors
```bash
grep "ERROR" .empirica/sync.log | tail -20
```

### Count Synced Projects
```bash
grep "Discovered 17 project.yaml files total" .empirica/sync.log | tail -1
```

### Check Relationships
```bash
grep "owns projects:" .empirica/sync.log
```

### Verify Validations
```bash
grep "Validation:" .empirica/sync.log | tail -4
```

---

## One-Page Decision Flowchart

```
Question: Do I need to do something now?

├─ Is owner_contact_id populated in project.yaml?
│  ├─ NO → Populate owner_contact_id: aioshuman@gmail.com
│  │       Re-run sync
│  │       Verify relationships count > 0
│  └─ YES → Continue to next question
│
├─ Are relationships being discovered?
│  ├─ NO → Check sync.log for errors
│  │       Run: grep "ERROR" .empirica/sync.log
│  └─ YES → Continue to next question
│
├─ Are all validation checks passing?
│  ├─ NO → Fix the blocker (see Troubleshooting)
│  └─ YES → Ready to populate additional metadata
│
├─ Ready to add governance fields?
│  ├─ YES:
│  │  ├─ Add stakeholder_contact_ids to practices
│  │  ├─ Add mesh_role_id to practices
│  │  ├─ Add authority_tier_id to practices
│  │  └─ Re-run sync
│  └─ NO → Wait for Admiral approval (Gate 1)
│
└─ Ready for M2 Rank 1 tasks (AUTHORITY_MATRIX, etc.)?
   ├─ YES → Proceed to Task T2
   └─ NO → Continue Phase 5 activation
```

---

## Sync Results Interpretation

### Healthy Sync
```
2026-09-11 19:16:34 | INFO | === Entity Sync Pipeline Started ===
2026-09-11 19:16:34 | INFO | Discovered 17 project.yaml files total
2026-09-11 19:16:34 | INFO | Project synced: ... (17 logs)
2026-09-11 19:16:34 | INFO |   Result: {'created': 17, 'updated': 0, 'errors': 0}
2026-09-11 19:16:37 | INFO | Extracted 2 contacts from git log
2026-09-11 19:16:37 | INFO | Contact synced: email=..., name=...
2026-09-11 19:16:37 | INFO |   Result: {'created': 2, 'updated': 0, 'errors': 0, 'relationships': 0}
2026-09-11 19:16:38 | INFO | Validation: no_orphaned_relationships = PASS
2026-09-11 19:16:38 | INFO | Validation: no_duplicate_canonical_ids = PASS
2026-09-11 19:16:38 | INFO | Validation: all_authority_tiers_valid = PASS
2026-09-11 19:16:38 | INFO | Validation: all_references_resolve = PASS
2026-09-11 19:16:38 | INFO | ✓ All validations passed
2026-09-11 19:16:38 | INFO | === Entity Sync Pipeline Completed ===
```
**Action:** No action needed; mesh is healthy.

### After Activation (Expected)
```
...
2026-09-11 19:16:37 | INFO | Contact aioshuman@gmail.com owns projects: empirica-foundation-evaluator, empirica-temporal-oracle, ...
2026-09-11 19:16:37 | INFO |   Result: {'created': 2, 'updated': 0, 'errors': 0, 'relationships': 17}
...
```
**Action:** Verify relationships = 17; all projects have owners.

### With Orphaned Relationships
```
2026-09-11 19:16:38 | ERROR | Orphaned relationship: unknown@example.com → project_id (contact not found)
2026-09-11 19:16:38 | FAIL | Validation: no_orphaned_relationships = FAIL
```
**Action:** Fix owner_contact_id or add missing contact to registry.

### With Duplicate IDs
```
2026-09-11 19:16:38 | ERROR | Duplicate canonical ID: org-empirica-foundation.carly.humanaios
2026-09-11 19:16:38 | FAIL | Validation: no_duplicate_canonical_ids = FAIL
```
**Action:** Find two projects with same ai_id; rename one.

---

## Troubleshooting

### Problem: "Discovered 0 project.yaml files"

**Cause:** Path resolution issue  
**Fix:**
```bash
# Verify directory structure
ls -la /home/user/empirica-practice-mesh/practices/

# Check a specific practice
ls -la /home/user/empirica-practice-mesh/practices/empirica-foundation-evaluator/.empirica/
```

**Expected:** All practices have `.empirica/project.yaml`

---

### Problem: "Invalid project: Missing ai_id"

**Cause:** project.yaml missing required field  
**Fix:**
```bash
# Find problematic file
grep "Missing ai_id" .empirica/sync.log

# Edit the file and add:
ai_id: <practice-name>
```

**Required fields:** ai_id, org_id, project_id

---

### Problem: "Orphaned relationship"

**Cause:** Project lists owner but contact not in registry  
**Fix:**

Option A: Fix the owner_contact_id in project.yaml
```yaml
owner_contact_id: aioshuman@gmail.com  # Use known contact
```

Option B: Add the missing contact to registry
```bash
# Ensure contact has git commits or manual registry entry
# Re-run sync to discover
```

---

### Problem: "Duplicate canonical ID"

**Cause:** Two practices with same ai_id  
**Fix:**
```bash
# Find duplicates
grep "Duplicate canonical ID" .empirica/sync.log

# Identify practices with conflicting ai_id
# Rename one and re-run sync
```

---

### Problem: Sync runs but "relationships: 0"

**Cause:** owner_contact_id not populated  
**Fix:**
```bash
# Add to each practice's project.yaml:
owner_contact_id: aioshuman@gmail.com

# Re-run sync:
python3 scripts/sync_entity_registry.py

# Verify:
grep "owns projects:" .empirica/sync.log
```

---

## File Locations

| File | Purpose | Path |
|------|---------|------|
| Sync Script | Run pipeline | `/home/user/empirica-practice-mesh/scripts/sync_entity_registry.py` |
| Sync Log | View results | `/home/user/empirica-practice-mesh/.empirica/sync.log` |
| Practices | Edit project.yaml | `/home/user/empirica-practice-mesh/practices/*/` |
| MCP Adapter | Live queries | `/home/user/empirica-practice-mesh/.claude/mcp/empirica-registry.py` |
| Authority Rules | Evaluator rules | `/home/user/humanaios/docs/EVALUATOR_RULES.md` |
| Evaluator Seat | Role definition | `/home/user/humanaios/docs/EVALUATOR_SEAT.md` |

---

## What You Own as Evaluator

### Authority Decisions
- [ ] Approve relationship data population (Gate 1)
- [ ] Approve authority matrix structure (Gate 2)
- [ ] Decide mesh roles per practice
- [ ] Define stakeholder groups
- [ ] Assign authority tiers (Zone 1/2/3)

### Governance Documents
- [ ] AUTHORITY_MATRIX.yaml (M2 Rank 1 Task T2)
- [ ] ESCALATION_PROTOCOL.md (M2 Rank 1 Task T3)
- [ ] CLAUDE.md updates across practices (M2 Rank 1 Task T4)
- [ ] Ratification of Z3 system (M2 Rank 1 Task T5)

### Monitoring & Quality
- [ ] Review sync.log weekly for health
- [ ] Validate new practices before integration
- [ ] Investigate validation failures immediately
- [ ] Approve mesh role assignments
- [ ] Monitor temporal oracle coordination

---

## Key Contacts

| Role | Name | Email | Purpose |
|------|------|-------|---------|
| Admiral | Carly Anderson | aioshuman@gmail.com | Authority, governance approval |
| Evaluator | empirica-foundation-evaluator | — | Assessment & calibration |
| Claude | Claude AI | noreply@anthropic.com | Stakeholder in decisions |
| BDFL | David | — | Final code ownership |

---

## Next 3 Decisions for Evaluator

### Decision 1: Activate Relationships (IMMEDIATE)
**Question:** Should I populate owner_contact_id fields now?
- **If YES:** All practices owned by Carly
- **If NO:** Defer to manual review per practice
- **Timeline:** 30 minutes to populate + re-run

### Decision 2: Add Governance Metadata (SHORT-TERM)
**Question:** Ready to populate stakeholder_contact_ids and mesh_role_id?
- **If YES:** Provide mapping per practice
- **If NO:** Defer to after Gate 2
- **Timeline:** 1 hour to populate + re-run

### Decision 3: Create Authority Matrix (MEDIUM-TERM)
**Question:** Ready to define AUTHORITY_MATRIX.yaml?
- **If YES:** Define approval chains per decision type
- **If NO:** Defer to after relationship activation
- **Timeline:** 2–4 hours including Admiral review

---

## Checklists

### Phase 5 Activation Checklist
- [ ] Review HANDOFF_M2R3_PHASE5.md
- [ ] Understand pipeline architecture (PIPELINE_ARCHITECTURE.md)
- [ ] Approve Decision 1: Activate relationships
- [ ] Edit project.yaml files to add owner_contact_id
- [ ] Run: `python3 scripts/sync_entity_registry.py`
- [ ] Verify: relationships count > 0
- [ ] Confirm: all validation checks pass
- [ ] Sign off: Phase 5 complete

### M2 Rank 1 Preparation Checklist (Not Yet)
- [ ] Gather stakeholder input on governance structure
- [ ] Map each practice to mesh role (evaluator/coordinator/executor/etc.)
- [ ] Define authority tier per practice (Zone 1/2/3)
- [ ] Draft AUTHORITY_MATRIX.yaml
- [ ] Draft ESCALATION_PROTOCOL.md
- [ ] Schedule Admiral review (24–48h latency)

---

## Useful Queries

### "What practices exist?"
```bash
ls -1 /home/user/empirica-practice-mesh/practices/ | grep -v "^\." | sort
```

### "Who owns what?"
```bash
grep -r "owner_contact_id" /home/user/empirica-practice-mesh/practices/ --include="project.yaml"
```

### "Which practices have validation errors?"
```bash
grep "ERROR\|Invalid" .empirica/sync.log
```

### "What has changed since last sync?"
```bash
# Compare hashes to detect content changes
# (Currently logged but not compared; enhancement)
```

### "Are there any broken relationships?"
```bash
grep "Orphaned relationship:" .empirica/sync.log
```

---

## Emergency Contacts

**If sync fails completely:**
1. Check `sync.log` for ERROR or FAILED
2. Verify practices directory exists: `ls /home/user/empirica-practice-mesh/practices/`
3. Verify Python 3 installed: `python3 --version`
4. Verify yaml module: `python3 -c "import yaml; print(yaml.__version__)"`
5. Run with verbose output: `python3 -u scripts/sync_entity_registry.py 2>&1`

**If unable to fix:**
- This is a supervised pipeline; errors should be logged
- Do not manually edit registry unless instructed
- Contact pipeline author or Admiral for guidance

---

## One-Line Summaries

- **sync_entity_registry.py** = Discovers practices, validates schemas, establishes relationships, logs audit trail hourly
- **get_project_owner_contacts()** = Finds who owns what by reading project.yaml owner_contact_id fields
- **validate_all_syncs()** = Detects orphaned relationships, duplicate IDs, inconsistencies
- **AUTHORITY_MATRIX.yaml** = "If decision type X, then role Y must approve" (not yet created)
- **ESCALATION_PROTOCOL.md** = "When Zone 1 blocked, escalate to Zone 2 with rule Z" (not yet created)
- **Relationship linking** = Connecting contacts to practices; currently implemented, awaiting data population

---

**Last Updated:** 2026-09-11 19:16:38 UTC  
**Next Review:** After Phase 5 activation (owner_contact_id population)
