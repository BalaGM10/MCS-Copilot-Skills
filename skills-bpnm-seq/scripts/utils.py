# =============================================================================
# utils.py — Shared utilities for BPMN-to-Mermaid skill
# Version: 1.0.0
# Date: 2026-09-09
# Original Author: Bala Madhusoodhanan
# Enhanced By: Antigravity AI (Peer Coding)
# Changelog:
#   1.0.0 (2026-09-09) - Antigravity enhancement. Shape classification,
#                        ID sanitisation, dependency management, JSON IR I/O.
# =============================================================================

import re
import json
import subprocess
import sys
import importlib

def sanitize_id(text: str) -> str:
    """Convert labels to valid Mermaid node IDs (lowercase, alphanumeric + underscores, max 20 chars)."""
    if not text:
        return "node"
    s = re.sub(r'[^a-zA-Z0-9]+', '_', str(text).lower())
    s = s.strip('_')
    return s[:20] if s else "node"

def sanitize_label(text: str) -> str:
    """Escape special Mermaid characters in labels (quotes, brackets, pipes, etc.)."""
    if not text:
        return ""
    # Replace quotes, brackets, pipes, etc.
    s = str(text)
    s = s.replace('"', '\\"').replace('(', '\\(').replace(')', '\\)')
    s = s.replace('[', '\\[').replace(']', '\\]').replace('|', '\\|')
    return s

def classify_bpmn_shape(master_name: str) -> str:
    """Classify shape type from Visio master shape name."""
    if not master_name:
        return 'unknown'
    
    name = master_name.lower()
    
    if 'start event' in name or 'startevent' in name:
        return 'start_event'
    if 'end event' in name or 'endevent' in name:
        return 'end_event'
    if 'intermediate event' in name or 'intermediateevent' in name:
        return 'intermediate_event'
    if 'task' in name or 'activity' in name:
        return 'task'
    if 'sub-process' in name or 'subprocess' in name or 'sub_process' in name:
        return 'sub_process'
    if 'exclusive' in name:
        return 'exclusive_gateway'
    if 'parallel' in name:
        return 'parallel_gateway'
    if 'inclusive' in name:
        return 'inclusive_gateway'
    if 'gateway' in name:
        return 'exclusive_gateway'  # Default gateway
    if 'data object' in name or 'dataobject' in name:
        return 'data_object'
    if 'pool' in name:
        return 'pool'
    if 'lane' in name or 'swimlane' in name or 'functionband' in name:
        return 'lane'
    if 'sequence flow' in name or 'message flow' in name or 'connector' in name or 'dynamic connector' in name:
        return 'connector'
        
    return 'unknown'

def ensure_dependencies(*packages):
    """Auto-install required Python packages via pip if not present."""
    for package in packages:
        try:
            importlib.import_module(package)
        except ImportError:
            print(f"Installing missing package: {package}", file=sys.stderr)
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            except subprocess.CalledProcessError as e:
                print(f"Failed to install {package}: {e}", file=sys.stderr)

def load_json_ir(path: str) -> dict:
    """JSON IR I/O with validation."""
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def save_json_ir(data: dict, path: str):
    """Save JSON IR."""
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def generate_id(prefix: str, counter_dict: dict) -> str:
    """Generate unique IDs like 'task_1', 'gw_2'."""
    if prefix not in counter_dict:
        counter_dict[prefix] = 1
    else:
        counter_dict[prefix] += 1
    return f"{prefix}_{counter_dict[prefix]}"
