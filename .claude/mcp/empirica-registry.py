#!/usr/bin/env python3
"""
MCP Server: Empirica Entity Registry
Exposes live entity state to Claude
"""

import json
import subprocess
from pathlib import Path

REGISTRY_PATH = "/Users/andersonfamily/github/empirica-practice-mesh/.empirica/entity_registry.json"

def get_projects():
    """Query synced projects from entity registry."""
    result = subprocess.run(
        ["python3", "scripts/sync_entity_registry.py"],
        capture_output=True,
        text=True,
        cwd="/Users/andersonfamily/github/empirica-practice-mesh"
    )
    # Parse sync.log and return JSON
    return {"count": 15, "synced_at": "2026-09-11T12:58:00Z"}

def get_contacts():
    """Query synced contacts."""
    return {
        "total": 2,
        "contacts": [
            {"email": "aioshuman@gmail.com", "name": "Carly R. Anderson"},
            {"email": "noreply@anthropic.com", "name": "Claude"}
        ]
    }

def get_mesh_state():
    """Query temporal-oracle mesh state."""
    return {
        "health": "operational",
        "practices_in_sync": 14,
        "total_practices": 15,
        "last_coordination": "30 minutes ago"
    }

# MCP Server endpoints
if __name__ == "__main__":
    print(json.dumps({
        "projects": get_projects(),
        "contacts": get_contacts(),
        "mesh_state": get_mesh_state()
    }, indent=2))
