#!/usr/bin/env python3
import sys
import json
from datetime import datetime, timedelta

WINDOW = timedelta(minutes=15)
SEV_RANK = {"low": 0, "medium": 1, "high": 2, "critical": 3}

REQUIRED_MIN_KEYS = ("ts", "hostname", "agent_id", "severity")

def parse_ts(ts_str):
    # Handle ISO 8601 with Z
    # datetime.fromisoformat supports "+00:00", so convert Z to that
    if ts_str.endswith("Z"):
        ts_str = ts_str[:-1] + "+00:00"
    return datetime.fromisoformat(ts_str)

def best_key(entry):
    # Choose the most specific identifier available
    sha256 = entry.get("sha256")
    threat = entry.get("threat_id")
    host = entry.get("hostname")

    if sha256:
        return f"sha256:{sha256}"
    if threat:
        return f"threat:{threat}"
    return f"host:{host}"

def validate_entry(entry):
    # Ensure required fields exist and are well formed
    for k in REQUIRED_MIN_KEYS:
        if k not in entry:
            return False
    if entry["severity"] not in SEV_RANK:
        return False
    try:
        parse_ts(entry["ts"])
    except Exception:
        return False
    return True

def should_update_kept(new_rank, new_ts, kept_rank, kept_ts):
    if new_rank > kept_rank:
        return True
    if new_rank == kept_rank and new_ts < kept_ts:
        return True
    return False

def emit_record(kept_event, key_str, suppressed_count, out_list):
    # kept_event is the dict we stored
    out_list.append((
        parse_ts(kept_event["ts"]),              # for sorting
        kept_event["ts"],                        # for printing
        kept_event["hostname"],
        kept_event["agent_id"],
        key_str,
        kept_event["severity"],
        suppressed_count
    ))

def process_file(path):
    active = {}  # key_str -> {window_start, kept_event, kept_rank, kept_ts, suppressed}
    emitted = [] # list of tuples as prepared in emit_record

    with open(path, "r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line:
                continue

            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue

            if not validate_entry(entry):
                continue

            try:
                evt_ts = parse_ts(entry["ts"])
            except Exception:
                continue

            key_str = best_key(entry)
            rank = SEV_RANK.get(entry["severity"])
            if key_str not in active:
                # Start a new window
                active[key_str] = {
                    "window_start": evt_ts,
                    "kept_event": entry,
                    "kept_rank": rank,
                    "kept_ts": evt_ts,
                    "suppressed": 0
                }
                continue

            slot = active[key_str]
            # Check window
            if evt_ts - slot["window_start"] <= WINDOW:
                # Inside window
                # Count this alert as part of the window
                slot["suppressed"] += 1
                # Promote kept if needed
                if should_update_kept(rank, evt_ts, slot["kept_rank"], slot["kept_ts"]):
                    slot["kept_event"] = entry
                    slot["kept_rank"] = rank
                    slot["kept_ts"] = evt_ts
            else:
                # Window expired. Emit, then start a new one.
                emit_record(slot["kept_event"], key_str, slot["suppressed"], emitted)
                active[key_str] = {
                    "window_start": evt_ts,
                    "kept_event": entry,
                    "kept_rank": rank,
                    "kept_ts": evt_ts,
                    "suppressed": 0
                }

    # Flush remaining windows
    for key_str, slot in active.items():
        emit_record(slot["kept_event"], key_str, slot["suppressed"], emitted)

    # Sort by hostname then ts
    emitted.sort(key=lambda r: (r[2], r[0]))

    # Print CSV rows (no header, to match the example)
    for _, ts_str, hostname, agent_id, key_str, kept_sev, suppressed in emitted:
        print(f"{ts_str},{hostname},{agent_id},{key_str},{kept_sev},{suppressed}")

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <alerts.log>")
        sys.exit(1)
    process_file(sys.argv[1])

if __name__ == "__main__":
    main()
