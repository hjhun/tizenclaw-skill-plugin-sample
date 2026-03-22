---
name: get_sample_info
description: Get sample device information including device name, OS version, architecture, and uptime
---

# Get Sample Info

Returns basic device information by reading platform metadata and system files.

## When to Use

Use this skill when the user asks about:
- Device name or hostname
- Operating system version
- CPU architecture
- System uptime

## Parameters

This skill requires no input parameters.

## Output

| Field | Type | Description |
|-------|------|-------------|
| `device_name` | string | Device hostname |
| `os_version` | string | OS platform string |
| `architecture` | string | CPU architecture (e.g., `x86_64`, `aarch64`) |
| `python_version` | string | Python runtime version |
| `uptime` | string | System uptime (e.g., `12h 34m`) |
