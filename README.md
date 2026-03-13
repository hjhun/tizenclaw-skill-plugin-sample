<p align="center">
  <strong>TizenClaw Skill Plugin Sample</strong>
</p>

<p align="center">
  Sample RPK skill plugin for TizenClaw — demonstrating how to extend the AI agent with containerized skill tools in Python, Node.js, and native C++.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/License-Apache_2.0-blue.svg" alt="License">
  <img src="https://img.shields.io/badge/Language-Python_%7C_Node.js_%7C_C%2B%2B-orange.svg" alt="Language">
  <img src="https://img.shields.io/badge/Platform-Tizen_10.0%2B-brightgreen.svg" alt="Platform">
  <img src="https://img.shields.io/badge/Skills-4_Multi--Runtime-purple.svg" alt="Skills">
</p>

---

## Overview

This project provides a sample **RPK (Resource Package) skill plugin** for [TizenClaw](https://github.com/hjhun/tizenclaw), the AI-powered agent daemon for Tizen OS. It demonstrates how to create skill tools in multiple runtimes that TizenClaw's LLM agent can invoke to query device information.

RPK skill plugins are distributed as Tizen resource packages and run in **sandboxed containers** managed by TizenClaw's `SkillPluginManager`. Each skill includes a **manifest.json** that defines the LLM tool schema (name, description, parameters) and an entry point script or binary.

### Included Skills

| Skill | Runtime | Description |
|-------|---------|-------------|
| `get_sample_info` | Python | Query device name, OS version, architecture, and uptime |
| `get_sample_status` | Python | Query CPU load, memory usage, and disk usage (supports `verbose` parameter) |
| `get_sample_time_node` | Node.js | Get system time information (ISO timestamp, timezone, Unix timestamp) |
| `get_sample_load_native` | Native C++ | Get system load averages and uptime via `/proc` filesystem |

---

## Quick Start

### Prerequisites

- Tizen GBS build environment ([installation guide](https://docs.tizen.org/platform/developing/installing/))
- `sdb` connected to a Tizen 10.0+ device or emulator
- [TizenClaw](https://github.com/hjhun/tizenclaw) daemon installed on the target device

### Automated Build & Deploy

```bash
# Full pipeline: build → deploy → register
./deploy.sh

# Quick rebuild (skip build-env init)
./deploy.sh -n

# Deploy existing RPM (skip build)
./deploy.sh -s

# Preview all steps without executing
./deploy.sh --dry-run
```

### Manual Build

```bash
# Build RPM package
gbs build -A x86_64 --include-all

# Deploy to device
sdb root on && sdb shell mount -o remount,rw /
sdb push ~/GBS-ROOT/local/repos/tizen/x86_64/RPMS/tizenclaw-skill-plugin-sample-1.1.0-1.x86_64.rpm /tmp/
sdb shell rpm -Uvh --force --nodeps /tmp/tizenclaw-skill-plugin-sample-1.1.0-1.x86_64.rpm

# Register with unified-backend and restart TizenClaw
sdb shell unified-backend --preload -y org.tizen.tizenclaw-skill-plugin-sample
sdb shell systemctl restart tizenclaw
```

---

## Usage

Once deployed, TizenClaw's LLM agent automatically discovers and registers the skills. You can verify the skills are loaded by checking the daemon logs:

```bash
sdb shell dlogutil TIZENCLAW
```

The agent can now invoke these skills through natural language queries. For example:

- *"What is the device info?"* → calls `get_sample_info`
- *"What is the system CPU and memory status?"* → calls `get_sample_status`
- *"What time is it?"* → calls `get_sample_time_node`
- *"What are the current load averages?"* → calls `get_sample_load_native`

### Direct Skill Testing

Skills can also be tested directly on the device:

```bash
# Python skill
sdb shell "cd /usr/apps/org.tizen.tizenclaw-skill-plugin-sample/lib/get_sample_info && python3 skill.py"

# Python skill with parameters
sdb shell "cd /usr/apps/org.tizen.tizenclaw-skill-plugin-sample/lib/get_sample_status && CLAW_ARGS='{\"verbose\":true}' python3 skill.py"

# Node.js skill
sdb shell "cd /usr/apps/org.tizen.tizenclaw-skill-plugin-sample/lib/get_sample_time_node && node skill.js"

# Native C++ skill
sdb shell /usr/apps/org.tizen.tizenclaw-skill-plugin-sample/lib/get_sample_load_native/get_sample_load_native
```

All skills output **JSON** to stdout for parsing by TizenClaw's LLM agent.

---

## How It Works

TizenClaw discovers RPK skill plugins through Tizen's package metadata system:

1. **Metadata Declaration** — Skills are registered in `tizen-manifest.xml` with the `http://tizen.org/metadata/tizenclaw/skill` metadata key
2. **Plugin Discovery** — TizenClaw's `SkillPluginManager` scans installed packages for this metadata via `pkgmgrinfo_appinfo_metadata_filter`
3. **Skill Loading** — Each skill directory's `manifest.json` is read to extract the LLM tool schema
4. **LLM Integration** — Tool schemas are registered as available tools, enabling the agent to invoke skills via the appropriate runtime executor (Python, Node.js, or native binary)

### Skill Execution Flow

```
User query → LLM selects skill → SkillPluginManager routes to runtime
  → Python: python3 <entry_point> (CLAW_ARGS env)
  → Node.js: node <entry_point> (CLAW_ARGS env)
  → Native:  ./<binary> (CLAW_ARGS env)
→ JSON output → LLM formats response
```

> **Note**: RPK packages are signed with a **platform-level certificate** and registered via `unified-backend` during deployment.

---

## Project Structure

```
tizenclaw-skill-plugin-sample/
├── lib/
│   ├── get_sample_info/              # Skill ① (Python)
│   │   ├── manifest.json             # LLM tool schema
│   │   └── skill.py                  # Skill implementation
│   ├── get_sample_status/            # Skill ② (Python)
│   │   ├── manifest.json
│   │   └── skill.py
│   ├── get_sample_time_node/         # Skill ③ (Node.js)
│   │   ├── manifest.json
│   │   └── skill.js
│   └── get_sample_load_native/       # Skill ④ (Native C++)
│       ├── manifest.json
│       └── main.cc
├── packaging/
│   ├── tizen-manifest.xml            # RPK manifest with skill metadata
│   ├── tizenclaw-skill-plugin-sample.spec
│   └── tizenclaw-skill-plugin-sample.manifest
├── docs/
│   ├── GUIDE.md                      # Development guide (English)
│   └── ko/
│       └── GUIDE.md                  # Development guide (Korean)
├── CMakeLists.txt
├── deploy.sh                         # Automated build & deploy script
└── README.md
```

---

## Creating Your Own Skill Plugin

For a step-by-step guide on creating new RPK skill plugins, see:

- 📖 [Development Guide (English)](docs/GUIDE.md)
- 📖 [개발 가이드 (한국어)](docs/ko/GUIDE.md)

---

## Related Projects

- [TizenClaw](https://github.com/hjhun/tizenclaw) — The core AI agent daemon for Tizen OS
- [tizenclaw-rag](https://github.com/hjhun/tizenclaw-rag) — On-device RAG knowledge base
- [tizenclaw-cli-plugin-sample](https://github.com/hjhun/tizenclaw-cli-plugin-sample) — Sample CLI tool plugin (native executables)
- [tizenclaw-llm-plugin-sample](https://github.com/hjhun/tizenclaw-llm-plugin-sample) — Sample LLM backend plugin (RPK)

---

## License

This project is licensed under the [Apache License 2.0](LICENSE).

Copyright 2024-2026 Samsung Electronics Co., Ltd.
