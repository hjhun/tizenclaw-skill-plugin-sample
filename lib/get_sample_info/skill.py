#!/usr/bin/env python3
"""get_sample_info skill - Returns sample device information."""

import json
import os
import platform


def main():
    """Return sample device information."""
    result = {
        "device_name": platform.node(),
        "os_version": platform.platform(),
        "architecture": platform.machine(),
        "python_version": platform.python_version(),
    }

    # Read uptime if available
    try:
        with open("/proc/uptime", "r") as f:
            uptime_seconds = float(f.read().split()[0])
            hours = int(uptime_seconds // 3600)
            minutes = int((uptime_seconds % 3600) // 60)
            result["uptime"] = f"{hours}h {minutes}m"
    except (FileNotFoundError, ValueError):
        result["uptime"] = "unknown"

    print(json.dumps(result))


if __name__ == "__main__":
    main()
