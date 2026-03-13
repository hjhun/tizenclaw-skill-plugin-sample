# TizenClaw Skill Plugin Sample

TizenClaw에 RPK를 통해 스킬(Tool)을 주입하는 샘플 프로젝트입니다.

## 구조

```
tizenclaw-skill-plugin-sample/
├── CMakeLists.txt
├── packaging/
│   ├── tizen-manifest.xml          # 메타데이터 선언
│   ├── tizenclaw-skill-plugin-sample.spec
│   └── tizenclaw-skill-plugin-sample.manifest
├── lib/
│   ├── get_sample_info/            # 스킬 ①
│   │   ├── manifest.json           # 스킬 정의 (LLM tool schema)
│   │   └── skill.py                # 스킬 구현
│   └── get_sample_status/          # 스킬 ②
│       ├── manifest.json
│       └── skill.py
└── README.md
```

## 메타데이터 선언

`tizen-manifest.xml`에서 다음과 같이 스킬을 등록합니다:

```xml
<metadata key="http://tizen.org/metadata/tizenclaw/skill"
          value="get_sample_info|get_sample_status"/>
```

- **key**: `http://tizen.org/metadata/tizenclaw/skill` (고정)
- **value**: `lib/` 아래의 스킬 디렉토리 이름을 `|`로 구분

### 대안: 여러 metadata 항목으로 선언

```xml
<metadata key="http://tizen.org/metadata/tizenclaw/skill" value="get_sample_info"/>
<metadata key="http://tizen.org/metadata/tizenclaw/skill" value="get_sample_status"/>
```

## 스킬 manifest.json 포맷

각 스킬의 `manifest.json`은 LLM tool schema를 따릅니다:

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

## 빌드 및 배포

```bash
gbs build -A armv7l --include-all
```

패키지가 설치되면 TizenClaw `SkillPluginManager`가 자동으로
스킬 디렉토리를 감지하고 LLM에 tool로 등록합니다.

## 라이선스

Apache-2.0
