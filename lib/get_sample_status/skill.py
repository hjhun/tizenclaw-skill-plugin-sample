#!/usr/bin/env python3
"""get_sample_status skill - Returns system status information."""

import json
import os


def get_cpu_load():
    """Read CPU load averages."""
    try:
        with open("/proc/loadavg", "r") as f:
            parts = f.read().split()
            return {
                "load_1min": float(parts[0]),
                "load_5min": float(parts[1]),
                "load_15min": float(parts[2]),
            }
    except (FileNotFoundError, ValueError, IndexError):
        return {"error": "unable to read CPU load"}


def get_memory_info():
    """Read memory usage from /proc/meminfo."""
    try:
        info = {}
        with open("/proc/meminfo", "r") as f:
            for line in f:
                parts = line.split()
                key = parts[0].rstrip(":")
                if key in ("MemTotal", "MemAvailable", "MemFree"):
                    info[key] = int(parts[1])  # in kB
        total = info.get("MemTotal", 0)
        available = info.get("MemAvailable", info.get("MemFree", 0))
        used = total - available
        return {
            "total_mb": round(total / 1024, 1),
            "used_mb": round(used / 1024, 1),
            "available_mb": round(available / 1024, 1),
            "usage_percent": round(used / total * 100, 1) if total else 0,
        }
    except (FileNotFoundError, ValueError):
        return {"error": "unable to read memory info"}


def get_disk_usage():
    """Get root filesystem disk usage."""
    try:
        stat = os.statvfs("/")
        total = stat.f_blocks * stat.f_frsize
        free = stat.f_bfree * stat.f_frsize
        used = total - free
        return {
            "total_mb": round(total / (1024 * 1024), 1),
            "used_mb": round(used / (1024 * 1024), 1),
            "free_mb": round(free / (1024 * 1024), 1),
            "usage_percent": round(used / total * 100, 1) if total else 0,
        }
    except OSError:
        return {"error": "unable to read disk usage"}


def main():
    """Return system status information."""
    args_str = os.environ.get("CLAW_ARGS", "{}")
    args = json.loads(args_str)
    verbose = args.get("verbose", False)

    result = {
        "cpu": get_cpu_load(),
        "memory": get_memory_info(),
        "disk": get_disk_usage(),
    }

    if verbose:
        try:
            cpu_count = os.cpu_count() or 0
            result["cpu"]["cpu_count"] = cpu_count
        except Exception:
            pass

    print(json.dumps(result))


if __name__ == "__main__":
    main()
