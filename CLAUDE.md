# empirica-practice-mesh — CLAUDE.md

## Authority & Governance

@docs/EVALUATOR_SEAT.md
@docs/EVALUATOR_RULES.md
@docs/AUTHORITY_MAPPING_Z3_EMPIRICA_V1.md

## Entity Registry (Live)

This workspace contains the empirica foundation's entity registry: 15 practices, 2+ contacts, governance hierarchy.

**Ground Truth:** `/Users/andersonfamily/practices`  
**GitHub Sync:** `humanaios-ui/empirica-practice-mesh`  
**Entity Discovery:** `python3 scripts/sync_entity_registry.py`

## Practice Manifest

All 15 registered practices (project.yaml in `.empirica/`):

- empirica-foundation-evaluator (Admiral seat — Carly R. Anderson)
- empirica-autonomy
- empirica-mesh-support
- empirica-outreach
- empirica-resource-miner
- humanaios
- humanaios-internal
- acat-x
- collaborator-ops
- opportunity-aggregator
- local-machine-optimizer
- grok-crossref
- schema.sql
- website
- flta-app-empirica

## Temporal Oracle Integration

**Live mesh coordination:** Every 30 minutes, empirica-temporal-oracle detects drift and broadcasts guidance.

When you query Claude in this workspace, you're querying a context that knows:
- Current mesh health (14/15 in sync)
- Active practices + contacts
- Authority tier relationships
- Engagement state

## MCP: Empirica Entity Registry

Claude can query live entity state via MCP:
mcp://empirica/entity_registry
├── projects (15 total, synced)
├── contacts (2+ total, extracted from git)
├── engagements (queried from DB)
└── organizations (static: empirica-foundation + empirica)

## Mesh Coordination
Claude is mesh-aware:
- Reads empirica-temporal-oracle state
- Understands practice interdependencies
- Can trigger mesh-support for GitHub issues
- Integrated with INTENT-OS automation
## Skills
- humanaios-findings-scan (detect calibration gaps)
- humanaios-wgs-sweep (audit governance state)
- humanaios-receipt-reconciliation (verify entity registry)
---
Last synced: 2026-09-11 12:58  
Entity count: 15 practices + 2 contacts  
Validation: ✓ All checks passing
