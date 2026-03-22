---
name: get_sample_status
description: Get sample system status including CPU load, memory usage, and disk usage
---

# Get Sample Status

Returns system resource usage statistics by reading `/proc` filesystem entries and running standard system queries.

## When to Use

Use this skill when the user asks about:
- CPU load or usage
- Memory (RAM) usage
- Disk space usage
- Overall system health or resource status

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `verbose` | boolean | No | If true, include detailed per-CPU statistics |

## Output

| Field | Type | Description |
|-------|------|-------------|
| `cpu_load_1m` | float | 1-minute CPU load average |
| `cpu_load_5m` | float | 5-minute CPU load average |
| `cpu_load_15m` | float | 15-minute CPU load average |
| `memory_total_mb` | int | Total RAM in MB |
| `memory_used_mb` | int | Used RAM in MB |
| `memory_percent` | float | RAM usage percentage |
| `disk_total_gb` | float | Total disk space in GB |
| `disk_used_gb` | float | Used disk space in GB |
| `disk_percent` | float | Disk usage percentage |
