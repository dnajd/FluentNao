#!/usr/bin/env python3
"""
Monitor Claude session files and push events to the FluentNao event bus.

Watches ~/.claude/projects/ for new or growing .jsonl session files.
Posts to POST /emit on the FluentNao server when activity is detected.

Events emitted:
  claude_session_activity  — existing Claude session got new content
  claude_session_new       — a new Claude session file appeared

Each event value is a JSON string: {"session": "<short_id>", "label": "<first_user_msg>", "bytes_added": N}
"""

import glob
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error

SESSIONS_DIR = os.path.expanduser("~/.claude/projects/-Users-donnajd-code")
NAO_SERVER = os.environ.get("NAO_SERVER", "http://localhost:5050")
POLL_INTERVAL = int(os.environ.get("SESSION_MONITOR_INTERVAL", "120"))  # 2 minutes


def log(msg):
    print("[session_monitor] {}".format(msg), flush=True)


def emit(event, value):
    script = "nao.emit({}, {})".format(repr(event), repr(value))
    req = urllib.request.Request(
        "{}/exec".format(NAO_SERVER),
        data=script.encode("utf-8"),
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            result = json.loads(resp.read())
            return result.get("ok", False)
    except Exception as e:
        log("emit failed: {}".format(e))
        return False


def session_label(path):
    """Extract the first meaningful user message as a label."""
    try:
        with open(path, "r", errors="replace") as f:
            for line in f:
                try:
                    d = json.loads(line)
                    msg = d.get("message", {})
                    if msg.get("role") == "user":
                        content = msg.get("content", "")
                        if isinstance(content, list):
                            text = " ".join(
                                p.get("text", "")
                                for p in content
                                if isinstance(p, dict) and p.get("type") == "text"
                            )
                        else:
                            text = str(content)
                        text = re.sub(r"<[^>]+>", " ", text).strip()
                        text = re.sub(r"\s+", " ", text)[:60]
                        if text:
                            return text
                except Exception:
                    continue
    except Exception:
        pass
    return os.path.basename(path)[:8]


def snapshot():
    sizes = {}
    for path in glob.glob(os.path.join(SESSIONS_DIR, "*.jsonl")):
        try:
            sizes[path] = os.path.getsize(path)
        except OSError:
            pass
    return sizes


def short_id(path):
    return os.path.basename(path)[:8]


def main():
    log("Starting. Watching {}".format(SESSIONS_DIR))
    log("Poll interval: {}s  NAO server: {}".format(POLL_INTERVAL, NAO_SERVER))

    sizes = snapshot()
    log("Tracking {} existing sessions".format(len(sizes)))

    while True:
        time.sleep(POLL_INTERVAL)
        try:
            new_sizes = snapshot()
            new_paths = set(new_sizes) - set(sizes)

            # new sessions
            for path in sorted(new_paths):
                label = session_label(path)
                log("New session {}: {}".format(short_id(path), label))
                emit("claude_session_new", json.dumps({
                    "session": short_id(path),
                    "label": label,
                    "bytes": new_sizes[path],
                }))
                sizes[path] = new_sizes[path]

            # existing sessions with new content
            changed = []
            for path, old_size in list(sizes.items()):
                new_size = new_sizes.get(path, old_size)
                if new_size > old_size:
                    label = session_label(path)
                    diff = new_size - old_size
                    log("Activity in {}: +{} bytes  ({})".format(short_id(path), diff, label))
                    changed.append({
                        "session": short_id(path),
                        "label": label,
                        "bytes_added": diff,
                    })
                    sizes[path] = new_size

            if changed:
                # emit one event per changed session
                for info in changed:
                    emit("claude_session_activity", json.dumps(info))

        except Exception as e:
            log("Error: {}".format(e))


if __name__ == "__main__":
    main()
