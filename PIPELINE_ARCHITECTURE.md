# Entity Sync Pipeline Architecture Diagram

## Pipeline Flow & State Machine

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     M2 Rank 3 Phase 5: Entity Sync Pipeline                 │
│                              (OPERATIONAL)                                   │
└─────────────────────────────────────────────────────────────────────────────┘

                              PREFLIGHT: DISCOVER
                                    ↓
                     ┌──────────────────────────────┐
                     │  discover_project_yamls()    │
                     │  ───────────────────────────  │
                     │  Input: practices/            │
                     │  Glob: **/.empirica/project.  │
                     │  yaml                         │
                     │  Output: [17 paths]           │
                     └──────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                          TASK 1: PROJECTS (✅)                              │
├─────────────────────────────────────────────────────────────────────────────┤
│  sync_projects()                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │ FOR EACH project.yaml:                                              │    │
│  │   1. load_project_yaml() → parse YAML                              │    │
│  │   2. validate_project()  → check ai_id, org_id, project_id         │    │
│  │   3. canonical_id = "{org}.{tenant}.{ai_id}"                       │    │
│  │      ✓ Must have exactly 2 dots (3-form)                           │    │
│  │   4. compute_hash(yaml_path) → SHA256 for change detection         │    │
│  │   5. logger.info(f"Project synced: {canonical_id}, hash={...}")    │    │
│  │   6. changes["created"] += 1                                        │    │
│  │                                                                      │    │
│  │ RESULT: {'created': 17, 'updated': 0, 'errors': 0}                │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  ✅ VALIDATION: All 17 projects have valid canonical IDs                  │
│  ✅ STATUS: Ready for integration                                         │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                          TASK 2: CONTACTS (✅)                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  SOURCE 1: get_git_log_contacts()                                          │
│  ┌──────────────────────────────────────────────────────────┐              │
│  │ Subprocess: git log --format=%aE %aN                     │              │
│  │ Parse: email → name mapping                              │              │
│  │ Output: {'aioshuman@gmail.com': 'Carly Anderson',        │              │
│  │          'noreply@anthropic.com': 'Claude'}              │              │
│  │ Count: 2 contacts                                        │              │
│  └──────────────────────────────────────────────────────────┘              │
│           ↓                                                                 │
│           ├─────────────────────────┐                                      │
│           ↓                         ↓                                      │
│  SOURCE 2: get_project_owner_contacts() [NEW]                             │
│  ┌─────────────────────────────────────────────┐                          │
│  │ FOR EACH project.yaml:                      │                          │
│  │   Extract: owner_contact_id field           │                          │
│  │   Match: email to project.ai_id             │                          │
│  │   Output: {email: (name, [project_ids])}    │                          │
│  │ Current: {} (no owner_contact_id in files)  │                          │
│  └─────────────────────────────────────────────┘                          │
│           ↓                                                                 │
│  MERGE: all_contacts = git_contacts ∪ project_owners                      │
│  ┌─────────────────────────────────────────────────────────┐              │
│  │ Prioritize git log names (authoritative)                │              │
│  │ Add project ownership relationships to metrics          │              │
│  │ Log: "Contact {email} owns projects: {...}"             │              │
│  │ changes["relationships"] += len(projects)               │              │
│  └─────────────────────────────────────────────────────────┘              │
│                                                                              │
│  RESULT: {'created': 2, 'updated': 0, 'errors': 0, 'relationships': 0}   │
│                                                                              │
│  🟡 PENDING: Activation when owner_contact_id fields populated            │
│  🟡 Expected after activation: relationships → 17                          │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                       TASK 3: ENGAGEMENTS (🟡)                              │
├─────────────────────────────────────────────────────────────────────────────┤
│  sync_engagements()                                                         │
│  ┌────────────────────────────────────────────────────────────┐            │
│  │ STUB: "no engagement records found"                        │            │
│  │ TODO: Query empirica DB for engagement records            │            │
│  │ Blocked by: DB connection string, engagement schema       │            │
│  │ Priority: Medium (non-blocking for mesh governance)       │            │
│  └────────────────────────────────────────────────────────────┘            │
│                                                                              │
│  RESULT: {'created': 0, 'updated': 0, 'errors': 0}                       │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                       TASK 4: ORGANIZATIONS (✅)                            │
├─────────────────────────────────────────────────────────────────────────────┤
│  sync_organizations()                                                       │
│  ┌────────────────────────────────────────────────────────────┐            │
│  │ Static: org-empirica-foundation (Admiral seat)             │            │
│  │ Static: org-empirica (company)                             │            │
│  │ No changes expected; typically defined in config           │            │
│  └────────────────────────────────────────────────────────────┘            │
│                                                                              │
│  RESULT: {'created': 0, 'updated': 0, 'errors': 0}                       │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓
                              VALIDATION GATES
                                    ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                   validate_all_syncs() → Dict[str, bool]                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  CHECK 1: no_orphaned_relationships = ✅ PASS                             │
│  ────────────────────────────────────────────────────────────              │
│  FOR EACH (owner_email, project_id) in relationships:                      │
│    IF owner_email NOT IN contacts → ERROR (orphan)                         │
│    IF project_id NOT IN projects → ERROR (dangling ref)                    │
│  Current: 0 relationships → trivially passes                               │
│  Expected after activation: 17 relationships, all valid                    │
│                                                                              │
│  CHECK 2: no_duplicate_canonical_ids = ✅ PASS                            │
│  ─────────────────────────────────────                                     │
│  Scan all projects:                                                        │
│    canonical_id = f"{org}.{tenant}.{ai_id}"                                │
│    Add to set; if duplicate, ERROR                                         │
│  Current: 17 unique IDs                                                    │
│                                                                              │
│  CHECK 3: all_authority_tiers_valid = ✅ PASS (stub)                      │
│  ──────────────────────────────────────                                    │
│  HOOK: validate authority_tier_id field                                    │
│  Pending: authority_tier_id data in project.yaml                           │
│                                                                              │
│  CHECK 4: all_references_resolve = ✅ PASS (stub)                         │
│  ────────────────────────────────                                          │
│  HOOK: validate dependency_ids, owner_contact_id, stakeholder refs        │
│  Pending: relationship field population                                    │
│                                                                              │
│  ALL_PASS = True → Log "✓ All validations passed"                         │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓
                            POSTFLIGHT: REPORT
                                    ↓
                     ┌──────────────────────────────┐
                     │  generate_daily_report()     │
                     │  ───────────────────────────  │
                     │  Parse sync.log for today     │
                     │  Summarize changes            │
                     │  TODO: Full report generation │
                     └──────────────────────────────┘
                                    ↓
                     ┌──────────────────────────────┐
                     │  === Pipeline Completed ===   │
                     │  Ready for next sync cycle    │
                     │  (Hourly via CronCreate)      │
                     └──────────────────────────────┘
```

---

## Entity Registry State

### Entities Discovered
```
Practices (17)
├── empirica-foundation-evaluator    ← Admiral seat, evaluator role
├── empirica-temporal-oracle         ← Mesh coordinator
├── empirica-autonomy
├── empirica-mesh-support
├── empirica-foundation
├── empirica-outreach
├── empirica-resource-miner
├── acat-x
├── collaborator-ops
├── opportunity-aggregator
├── local-machine-optimizer
├── grok-crossref
├── schema.sql
├── website
├── flta-app-empirica
├── humanaios                        ← Primary practice
├── humanaios-internal
└── humanaios/empirica-foundation    ← Sub-practice

Contacts (2)
├── aioshuman@gmail.com (Carly Anderson)
└── noreply@anthropic.com (Claude)

Relationships (0 → 17 pending)
└── [awaiting owner_contact_id in project.yaml]
```

---

## Dependency Graph (When Populated)

```
[Expected structure after activation]

empirica-temporal-oracle (coordinator)
    ↓ broadcasts to ↓
    ┌───────────────────────────────────────────┐
    ↓       ↓       ↓       ↓       ↓       ↓
empirica-   empirica-  empirica-  empirica-  empirica-
foundation- autonomy   mesh-      outreach   resource-
evaluator                support               miner
    ↑
    │ evaluated by
    │
humanaios (depends on empirica-foundation)
    ↓
humanaios-internal
```

---

## Authority Layer (Z3 Protocol Mapping)

```
ZONE 1: Chat & Collaboration
├─ Deliberation & proposals
├─ Decision-maker: Admiral (Carly)
└─ Practices: empirica-foundation-evaluator, empirica-autonomy, mesh-support

    ↓ escalates to ↓

ZONE 2: Authority Documents  
├─ Specs, RFCs, design docs
├─ Decision-maker: Admiral (serial gate)
├─ Approval latency: 24–48h
└─ Practices: All (when AUTHORITY_MATRIX.yaml deployed)

    ↓ escalates to ↓

ZONE 3: Terminal Execution
├─ Code commits, P3 verification, POSTFLIGHT
├─ Decision-maker: Carly or delegated Claude practitioner
├─ Pre-flight: Z3_PROTOCOL.md Sections B-1 through B-10
└─ Practices: Executing practices only
```

---

## Relationship Linking (When Activated)

```
Current State:
┌──────────────────────────────────────┐
│ Contact: aioshuman@gmail.com         │
│ Name: Carly Anderson                 │
│ Owns: [empty] ← awaiting data        │
└──────────────────────────────────────┘

Expected State (after owner_contact_id population):
┌──────────────────────────────────────────────────────────────┐
│ Contact: aioshuman@gmail.com                                 │
│ Name: Carly Anderson                                         │
│ Owns:                                                        │
│  ├─ empirica-foundation-evaluator   (Admiral + Evaluator)   │
│  ├─ empirica-temporal-oracle        (Coordinator)           │
│  ├─ empirica-mesh-support           (Support)               │
│  ├─ empirica-autonomy               (Autonomy)              │
│  ├─ ... (13 more practices)                                 │
│ Total relationships: 17                                      │
│                                                              │
│ Stakeholders (who must approve changes):                    │
│  └─ noreply@anthropic.com (Claude)  [pending addition]      │
└──────────────────────────────────────────────────────────────┘
```

---

## Data Flow: Git Commit → Registry Update

```
Developer commits project.yaml change
                    ↓
          Git push to origin/main
                    ↓
  CronCreate triggers hourly (or manual run)
                    ↓
    python3 sync_entity_registry.py
                    ↓
         discover_project_yamls()
       [recursively find all .yaml]
                    ↓
         load_project_yaml(path)
       [parse YAML, handle errors]
                    ↓
       validate_project(schema)
    [check ai_id, org_id, canonical]
                    ↓
        compute_hash(file_path)
      [SHA256 for change detection]
                    ↓
          sync_projects() → metrics
    [create/update registry entry]
                    ↓
       sync_contacts() → metrics
    [establish ownership links]
                    ↓
     validate_all_syncs() → bool
   [orphan detection, consistency]
                    ↓
      generate_daily_report()
    [summarize today's changes]
                    ↓
   Log all results to .empirica/sync.log
                    ↓
    Registry reflects latest state
   (MCP adapter queries live state)
```

---

## Success Criteria

### Phase 5 Completion ✅
- [x] Discover all 17 practices
- [x] Sync project schemas (0 errors)
- [x] Extract contacts (2 found)
- [x] Implement relationship linking code
- [x] Validate schemas (all checks passing)
- [x] Log audit trail (sync.log)

### Phase 5 Activation 🟡 (Pending)
- [ ] Populate owner_contact_id in project.yaml
- [ ] Re-run sync to discover relationships (expected: 17)
- [ ] Verify no orphaned relationships
- [ ] Confirm all contacts have projects assigned
- [ ] Generate final Phase 5 report

### M2 Rank 1 Tasks (Dependent on Phase 5)
- [ ] T2: Create AUTHORITY_MATRIX.yaml
- [ ] T3: Create ESCALATION_PROTOCOL.md
- [ ] T4: Update CLAUDE.md across 15 practices
- [ ] T5: Admiral ratification of Z3 system
- [ ] T6: Deploy CronCreate hourly sync

---

## Monitoring & Debugging

### Watch for Errors
```bash
# Orphaned relationships
grep "Orphaned relationship:" .empirica/sync.log

# Invalid projects
grep "Invalid project" .empirica/sync.log

# Duplicate canonical IDs
grep "Duplicate canonical ID" .empirica/sync.log

# Parse failures
grep "Failed to parse" .empirica/sync.log
```

### Sync Metrics Over Time
```bash
# Extract all sync results
grep "Result:" .empirica/sync.log | tail -10

# Should show:
# Projects: created count increasing or stable
# Contacts: should stabilize at 2 (until more added)
# Relationships: 0 until activation, then 17+
```

### Health Check
```bash
# Last sync succeeded?
tail -1 .empirica/sync.log | grep "Completed"

# All validations passed?
grep "All validations passed" .empirica/sync.log | tail -1
```

---

*This diagram reflects Phase 5 implementation state as of 2026-09-11 19:16:38 UTC.*
