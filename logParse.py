import sys
import json

REQUIRED_KEYS = (
    "agent_id",
    "hostname",
    "status",
    "cpu_pct",
    "mem_pct",
    "last_checkin_sec",
)

def get_unhealthy_reasons(entry):
    reasons = []

    if entry.get("status") != "ok":
        reasons.append("status_not_ok")

    try:
        if float(entry.get("cpu_pct", 0)) > 85:
            reasons.append("high_cpu")
    except (TypeError, ValueError):
        pass

    try:
        if float(entry.get("mem_pct", 0)) > 90:
            reasons.append("high_mem")
    except (TypeError, ValueError):
        pass

    try:
        if int(entry.get("last_checkin_sec", 0)) > 300:
            reasons.append("stale_checkin")
    except (TypeError, ValueError):
        pass

    return reasons

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <logfile>")
        sys.exit(1)

    logfile = sys.argv[1]
    unhealthy = []

    with open(logfile, "r") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue

            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                # In a real script you might log this somewhere
                print(f"Skipping invalid JSON at line {line_no}")
                continue

            if any(k not in entry for k in REQUIRED_KEYS):
                continue

            reasons = get_unhealthy_reasons(entry)
            if reasons:
                reason_str = ",".join(reasons)
                log_str = (
                    f"hostname={entry['hostname']} "
                    f"agent_id={entry['agent_id']} "
                    f"reasons={reason_str}"
                )
                unhealthy.append(log_str)

    for row in sorted(unhealthy, key=lambda x: x.split()[0].split("=")[1]):
        print(row)

if __name__ == "__main__":
    main()
