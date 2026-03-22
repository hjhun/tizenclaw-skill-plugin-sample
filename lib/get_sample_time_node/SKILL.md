---
name: get_sample_time_node
description: Get system time information using Node.js including ISO timestamp and timezone
---

# Get Sample Time Node

Returns the current system time information using Node.js runtime. This demonstrates Node.js-based skill execution.

## When to Use

Use this skill when the user asks about:
- Current date and time
- Timezone information
- Unix timestamp

## Parameters

This skill requires no input parameters.

## Output

| Field | Type | Description |
|-------|------|-------------|
| `iso` | string | Current time in ISO 8601 format |
| `timezone` | string | System timezone name |
| `unix_timestamp` | int | Current Unix timestamp (seconds since epoch) |
