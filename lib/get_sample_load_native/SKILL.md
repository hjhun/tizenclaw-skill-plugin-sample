---
name: get_sample_load_native
description: Get system load averages and uptime using a native C++ binary via /proc filesystem
---

# Get Sample Load Native

Returns system load averages (1min, 5min, 15min) and uptime by reading `/proc/loadavg` and `/proc/uptime` directly from a compiled C++ binary. This demonstrates native runtime skill execution.

## When to Use

Use this skill when the user asks about:
- System load averages
- CPU load over time intervals
- System uptime (with high precision)

## Parameters

This skill requires no input parameters.

## Output

| Field | Type | Description |
|-------|------|-------------|
| `load_1m` | float | 1-minute load average |
| `load_5m` | float | 5-minute load average |
| `load_15m` | float | 15-minute load average |
| `uptime_seconds` | float | System uptime in seconds |
