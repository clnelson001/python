#!/usr/bin/env python3
import sys, json
from datetime import datetime, timedelta

def parse_ts(s: str) -> datetime:
    # Accept ISO 8601 with trailing Z
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    return datetime.fromisoformat(s)

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <agent_heartbeats.log>")
        sys.exit(1)

    path = sys.argv[1]
    latest = None
    errors = []  # store tuples of (ts, agent_id)

    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            s = raw.strip()
            if not s:
                continue
            try:
                rec = json.loads(s)
            except json.JSONDecodeError:
                continue

            ts_s = rec.get("ts")
            aid = rec.get("agent_id")
            status = rec.get("status")
            if not ts_s or not aid or status is None:
                continue

            try:
                ts = parse_ts(ts_s)
            except Exception:
                continue

            if latest is None or ts > latest:
                latest = ts

            if status == "error":
                errors.append((ts, aid))

    if latest is None:
        print("Unhealthy agents in last 10 min: []")
        return

    cutoff = latest - timedelta(minutes=10)
    recent_unhealthy = sorted({aid for ts, aid in errors if ts >= cutoff})
    print(f"Unhealthy agents in last 10 min: {recent_unhealthy}")

if __name__ == "__main__":
    main()
