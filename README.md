# TizenClaw Skill Plugin Sample

A sample project that injects skills (tools) into TizenClaw via RPK (Resource Package).

## Structure

```
tizenclaw-skill-plugin-sample/
├── CMakeLists.txt
├── packaging/
│   ├── tizen-manifest.xml          # Metadata declaration
│   ├── tizenclaw-skill-plugin-sample.spec
│   └── tizenclaw-skill-plugin-sample.manifest
├── lib/
│   ├── get_sample_info/            # Skill ①
│   │   ├── manifest.json           # Skill definition (LLM tool schema)
│   │   └── skill.py                # Skill implementation
│   └── get_sample_status/          # Skill ②
│       ├── manifest.json
│       └── skill.py
└── README.md
```

## Metadata Declaration

Skills are registered in `tizen-manifest.xml` as follows:

```xml
<metadata key="http://tizen.org/metadata/tizenclaw/skill"
          value="get_sample_info|get_sample_status"/>
```

- **key**: `http://tizen.org/metadata/tizenclaw/skill` (fixed)
- **value**: Skill directory names under `lib/`, separated by `|`

### Alternative: Declaring with Multiple Metadata Entries

```xml
<metadata key="http://tizen.org/metadata/tizenclaw/skill" value="get_sample_info"/>
<metadata key="http://tizen.org/metadata/tizenclaw/skill" value="get_sample_status"/>
```

## Skill manifest.json Format

Each skill's `manifest.json` follows the LLM tool schema:

```json
{
  "name": "get_sample_info",
  "description": "Get sample device information",
  "category": "Device Info",
  "parameters": {
    "type": "object",
    "properties": {},
    "required": []
  },
  "entry_point": "skill.py"
}
```

## Build & Deploy

```bash
# Full build and deploy pipeline
./deploy.sh

# Quick rebuild (skip build-env init)
./deploy.sh -n

# Deploy existing RPM (skip build)
./deploy.sh -s

# See all options
./deploy.sh --help
```

Once the package is installed, the TizenClaw `SkillPluginManager` automatically
detects the skill directories and registers them as tools for the LLM.

## License

[Apache-2.0](LICENSE)
