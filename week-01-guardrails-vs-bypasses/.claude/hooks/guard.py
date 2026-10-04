#!/usr/bin/env python3
"""
Week 01 PreToolUse guard.

What it does
  1. Logs every tool call Claude Code is about to make to logs/audit.jsonl
  2. Denies any tool call whose input mentions a protected marker
  3. Fails closed. If anything goes wrong inside the hook it exits 2,
     which Claude Code treats as a block. Exit 1 would NOT block.

This guard is deliberately naive. It matches strings in the tool input,
so part of this week's exercise is finding the ways around it.
"""

import datetime
import json
import os
import sys

# Strings that should never appear in a tool call. Lowercase.
PROTECTED_MARKERS = ["secrets", ".env"]

# Keep log lines short so the audit trail does not become a copy of everything
MAX_LOGGED_CHARS = 500


def project_dir(event):
    return os.environ.get("CLAUDE_PROJECT_DIR") or event.get("cwd") or os.getcwd()


def write_audit(event, decision, reason):
    log_dir = os.path.join(project_dir(event), "logs")
    os.makedirs(log_dir, exist_ok=True)
    record = {
        "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "session_id": event.get("session_id"),
        "tool_name": event.get("tool_name"),
        "decision": decision,
        "reason": reason,
        "tool_input": json.dumps(event.get("tool_input", {}))[:MAX_LOGGED_CHARS],
    }
    with open(os.path.join(log_dir, "audit.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")


def find_marker(tool_input):
    # Flatten the whole input to text and look for any protected marker.
    # Normalise Windows separators so a backslash path still matches.
    text = json.dumps(tool_input).lower().replace("\\\\", "/")
    for marker in PROTECTED_MARKERS:
        if marker in text:
            return marker
    return None


def main():
    event = json.load(sys.stdin)
    tool_input = event.get("tool_input", {})
    marker = find_marker(tool_input)

    if marker:
        reason = f"Blocked by guard.py: tool input references protected marker '{marker}'"
        write_audit(event, "deny", reason)
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": reason,
            }
        }))
        return 0

    # No decision. The normal permission flow (deny rules, prompts) still applies.
    write_audit(event, "no-decision", "")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # fail closed on any error
        print(f"guard.py failed, blocking the call to be safe: {exc}", file=sys.stderr)
        sys.exit(2)
