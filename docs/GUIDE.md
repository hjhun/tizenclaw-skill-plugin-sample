# TizenClaw Skill Plugin Development Guide

This guide explains how to create RPK skill plugins for [TizenClaw](https://github.com/hjhun/tizenclaw). Skill plugins are resource packages (RPK) that extend the AI agent's capabilities with sandboxed tools written in Python, Node.js, or native C++.

---

## Concepts

### What is a Skill Plugin?

A skill plugin consists of one or more **skill directories**, each containing:

1. **manifest.json** — An LLM tool schema that defines the skill's name, description, parameters, and runtime
2. **Entry point** — A script (`skill.py`, `skill.js`) or native binary that executes the skill logic

TizenClaw's `SkillPluginManager` discovers installed skill plugins through Tizen's metadata system and registers them as tools for the LLM agent.

### Supported Runtimes

| Runtime | Entry Point | Language | Use Case |
|---------|-------------|----------|----------|
| `python` (default) | `skill.py` | Python 3 | General-purpose skills, system queries |
| `node` | `skill.js` | Node.js | Async operations, web APIs |
| `native` | Binary name | C/C++ | Performance-critical, low-level system access |

### How Discovery Works

```
RPK installed → unified-backend registers → pkgmgr event
→ SkillPluginManager scans metadata
→ reads manifest.json from each skill directory
→ registers tool schema with LLM agent
→ LLM invokes via runtime executor
```

---

## Step-by-Step: Adding a New Skill

### 1. Create the Skill Directory

Create a new directory under `lib/` with the skill files:

```
lib/
└── my_new_skill/
    ├── manifest.json
    └── skill.py         # or skill.js, or main.cc
```

### 2. Write manifest.json

The manifest defines how the LLM discovers and interacts with your skill:

```json
{
  "name": "my_new_skill",
  "description": "A clear description of what this skill does and what it returns.",
  "category": "Your Category",
  "parameters": {
    "type": "object",
    "properties": {
      "example_param": {
        "type": "string",
        "description": "Description of the parameter"
      }
    },
    "required": []
  },
  "entry_point": "skill.py"
}
```

**Key fields:**

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique skill name (must match the directory name) |
| `description` | Yes | Clear description for the LLM to understand when to use this skill |
| `category` | Yes | Grouping category (e.g., `"Device Info"`, `"Network"`) |
| `parameters` | Yes | JSON Schema for input parameters |
| `entry_point` | Yes | Script filename or binary name |
| `runtime` | No | `"python"` (default), `"node"`, or `"native"` |
| `language` | No | Required for native runtime: `"cpp"` or `"c"` |

### 3. Implement the Skill

#### Python Skill

```python
#!/usr/bin/env python3
"""my_new_skill - Description of the skill."""

import json
import os


def main():
    # Read parameters from CLAW_ARGS environment variable
    args_str = os.environ.get("CLAW_ARGS", "{}")
    args = json.loads(args_str)

    example_param = args.get("example_param", "default_value")

    # Perform the skill logic
    result = {
        "key": "value",
        "param_received": example_param,
    }

    # Output exactly one JSON line to stdout
    print(json.dumps(result))


if __name__ == "__main__":
    main()
```

#### Node.js Skill

Add `"runtime": "node"` to `manifest.json` and set `"entry_point": "skill.js"`:

```javascript
#!/usr/bin/env node
/**
 * my_new_skill - Description of the skill.
 * Reads CLAW_ARGS from environment for parameters.
 */

function main() {
  const argsStr = process.env.CLAW_ARGS || '{}';
  const args = JSON.parse(argsStr);

  const result = {
    key: 'value',
    param_received: args.example_param || 'default_value',
  };

  // Output exactly one JSON line to stdout
  console.log(JSON.stringify(result));
}

main();
```

#### Native C++ Skill

Add `"runtime": "native"` and `"language": "cpp"` to `manifest.json`. Set `"entry_point"` to the binary name:

```cpp
#include <cstdio>
#include <cstdlib>

int main() {
  // Read CLAW_ARGS from environment (if needed)
  // const char* args = getenv("CLAW_ARGS");

  printf("{\"key\": \"value\"}\\n");
  return 0;
}
```

### 4. Update CMakeLists.txt

#### For Python / Node.js skills

Add a directory install rule:

```cmake
INSTALL(DIRECTORY lib/my_new_skill/
    DESTINATION ${RPK_APP_DIR}/lib/my_new_skill
)
```

#### For native C++ skills

Add a build target and install rules:

```cmake
# Build native skill binary
ADD_EXECUTABLE(my_new_skill
  lib/my_new_skill/main.cc
)

# Install manifest + binary
INSTALL(FILES lib/my_new_skill/manifest.json
    DESTINATION ${RPK_APP_DIR}/lib/my_new_skill
)
INSTALL(TARGETS my_new_skill
    DESTINATION ${RPK_APP_DIR}/lib/my_new_skill
)
```

### 5. Update tizen-manifest.xml

Add the new skill name to the metadata value, separated by `|`:

```xml
<metadata key="http://tizen.org/metadata/tizenclaw/skill"
          value="get_sample_info|get_sample_status|get_sample_time_node|get_sample_load_native|my_new_skill"/>
```

Alternatively, add a separate metadata entry:

```xml
<metadata key="http://tizen.org/metadata/tizenclaw/skill" value="my_new_skill"/>
```

### 6. Update the Spec File

Add the new skill's files to the `%files` section in `packaging/tizenclaw-skill-plugin-sample.spec`:

```spec
# For Python / Node.js skills
/usr/apps/org.tizen.tizenclaw-skill-plugin-sample/lib/my_new_skill/manifest.json
/usr/apps/org.tizen.tizenclaw-skill-plugin-sample/lib/my_new_skill/skill.py

# For native skills (set executable permission)
/usr/apps/org.tizen.tizenclaw-skill-plugin-sample/lib/my_new_skill/manifest.json
%attr(755,root,root) /usr/apps/org.tizen.tizenclaw-skill-plugin-sample/lib/my_new_skill/my_new_skill
```

### 7. Build and Deploy

```bash
./deploy.sh
```

---

## Design Guidelines

### JSON Output

All skills MUST output valid JSON to stdout. This is critical for LLM parsing:

- **Success**: `{"key": "value", ...}`
- **Error**: `{"error": "descriptive message"}`
- Always output exactly **one line** of JSON

### Parameter Handling

Skills receive parameters via the `CLAW_ARGS` environment variable as a JSON string:

```python
import json, os
args = json.loads(os.environ.get("CLAW_ARGS", "{}"))
```

```javascript
const args = JSON.parse(process.env.CLAW_ARGS || '{}');
```

### manifest.json Best Practices

The `manifest.json` is what the LLM reads to understand your skill. Write descriptions that are:

- **Specific** — Tell the LLM exactly what data is returned
- **Action-oriented** — Start with a verb (e.g., "Get", "Query", "Check")
- **Context-rich** — Include return format hints in the description
- **Parameter-complete** — Document all parameters with clear descriptions and types

### Security

- RPK skill plugins MUST be signed with a **platform-level certificate**
- Skills are registered via `unified-backend --preload` during deployment
- Each skill runs in a sandboxed environment with limited system access

---

## Build Architecture Support

The project supports multiple architectures:

| Architecture | Target |
|-------------|--------|
| `x86_64` | Tizen Emulator |
| `armv7l` | 32-bit ARM devices |
| `aarch64` | 64-bit ARM devices |

```bash
# Build for specific architecture
./deploy.sh -a armv7l

# Build for emulator (default: auto-detect via sdb)
./deploy.sh
```
