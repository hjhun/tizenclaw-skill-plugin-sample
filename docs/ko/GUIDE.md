# TizenClaw 스킬 플러그인 개발 가이드

이 가이드는 [TizenClaw](https://github.com/hjhun/tizenclaw)용 RPK 스킬 플러그인을 개발하는 방법을 설명합니다. 스킬 플러그인은 Python, Node.js, 또는 네이티브 C++로 작성된 도구를 샌드박스 환경에서 실행하여 AI 에이전트의 기능을 확장하는 리소스 패키지(RPK)입니다.

---

## 개념

### 스킬 플러그인이란?

스킬 플러그인은 하나 이상의 **스킬 디렉토리**로 구성되며, 각 디렉토리에는 다음이 포함됩니다:

1. **manifest.json** — 스킬의 이름, 설명, 파라미터, 런타임을 정의하는 LLM 도구 스키마
2. **엔트리 포인트** — 스킬 로직을 실행하는 스크립트(`skill.py`, `skill.js`) 또는 네이티브 바이너리

TizenClaw의 `SkillPluginManager`는 Tizen의 메타데이터 시스템을 통해 설치된 스킬 플러그인을 탐색하고, LLM 에이전트의 도구로 등록합니다.

### 지원 런타임

| 런타임 | 엔트리 포인트 | 언어 | 사용 사례 |
|--------|-------------|------|----------|
| `python` (기본값) | `skill.py` | Python 3 | 범용 스킬, 시스템 조회 |
| `node` | `skill.js` | Node.js | 비동기 작업, 웹 API |
| `native` | 바이너리 이름 | C/C++ | 고성능, 저수준 시스템 접근 |

### 탐색 흐름

```
RPK 설치 → unified-backend 등록 → pkgmgr 이벤트
→ SkillPluginManager 메타데이터 스캔
→ 각 스킬 디렉토리의 manifest.json 읽기
→ LLM 에이전트에 도구 스키마 등록
→ LLM이 런타임 실행기를 통해 호출
```

---

## 단계별 가이드: 새로운 스킬 추가

### 1. 스킬 디렉토리 생성

`lib/` 하위에 스킬 파일들이 포함된 새 디렉토리를 생성합니다:

```
lib/
└── my_new_skill/
    ├── manifest.json
    └── skill.py         # 또는 skill.js, main.cc
```

### 2. manifest.json 작성

매니페스트는 LLM이 스킬을 탐색하고 상호작용하는 방식을 정의합니다:

```json
{
  "name": "my_new_skill",
  "description": "이 스킬이 하는 일과 반환하는 데이터에 대한 명확한 설명.",
  "category": "카테고리명",
  "parameters": {
    "type": "object",
    "properties": {
      "example_param": {
        "type": "string",
        "description": "파라미터에 대한 설명"
      }
    },
    "required": []
  },
  "entry_point": "skill.py"
}
```

**주요 필드:**

| 필드 | 필수 | 설명 |
|------|------|------|
| `name` | 예 | 고유한 스킬 이름 (디렉토리 이름과 일치해야 함) |
| `description` | 예 | LLM이 스킬 사용 시점을 판단할 수 있는 명확한 설명 |
| `category` | 예 | 그룹화 카테고리 (예: `"Device Info"`, `"Network"`) |
| `parameters` | 예 | 입력 파라미터의 JSON 스키마 |
| `entry_point` | 예 | 스크립트 파일명 또는 바이너리 이름 |
| `runtime` | 아니오 | `"python"` (기본값), `"node"`, 또는 `"native"` |
| `language` | 아니오 | 네이티브 런타임 시 필수: `"cpp"` 또는 `"c"` |

### 3. 스킬 구현

#### Python 스킬

```python
#!/usr/bin/env python3
"""my_new_skill - 스킬에 대한 설명."""

import json
import os


def main():
    # CLAW_ARGS 환경 변수에서 파라미터 읽기
    args_str = os.environ.get("CLAW_ARGS", "{}")
    args = json.loads(args_str)

    example_param = args.get("example_param", "default_value")

    # 스킬 로직 수행
    result = {
        "key": "value",
        "param_received": example_param,
    }

    # stdout으로 정확히 한 줄의 JSON 출력
    print(json.dumps(result))


if __name__ == "__main__":
    main()
```

#### Node.js 스킬

`manifest.json`에 `"runtime": "node"`를 추가하고 `"entry_point": "skill.js"`로 설정합니다:

```javascript
#!/usr/bin/env node
/**
 * my_new_skill - 스킬에 대한 설명.
 * 파라미터는 CLAW_ARGS 환경 변수에서 읽습니다.
 */

function main() {
  const argsStr = process.env.CLAW_ARGS || '{}';
  const args = JSON.parse(argsStr);

  const result = {
    key: 'value',
    param_received: args.example_param || 'default_value',
  };

  // stdout으로 정확히 한 줄의 JSON 출력
  console.log(JSON.stringify(result));
}

main();
```

#### 네이티브 C++ 스킬

`manifest.json`에 `"runtime": "native"`와 `"language": "cpp"`를 추가합니다. `"entry_point"`는 바이너리 이름으로 설정합니다:

```cpp
#include <cstdio>
#include <cstdlib>

int main() {
  // 필요시 CLAW_ARGS 환경 변수에서 파라미터 읽기
  // const char* args = getenv("CLAW_ARGS");

  printf("{\"key\": \"value\"}\n");
  return 0;
}
```

### 4. CMakeLists.txt 수정

#### Python / Node.js 스킬의 경우

디렉토리 설치 규칙을 추가합니다:

```cmake
INSTALL(DIRECTORY lib/my_new_skill/
    DESTINATION ${RPK_APP_DIR}/lib/my_new_skill
)
```

#### 네이티브 C++ 스킬의 경우

빌드 타겟과 설치 규칙을 추가합니다:

```cmake
# 네이티브 스킬 바이너리 빌드
ADD_EXECUTABLE(my_new_skill
  lib/my_new_skill/main.cc
)

# 매니페스트 + 바이너리 설치
INSTALL(FILES lib/my_new_skill/manifest.json
    DESTINATION ${RPK_APP_DIR}/lib/my_new_skill
)
INSTALL(TARGETS my_new_skill
    DESTINATION ${RPK_APP_DIR}/lib/my_new_skill
)
```

### 5. tizen-manifest.xml 수정

메타데이터 값에 새 스킬 이름을 `|`로 구분하여 추가합니다:

```xml
<metadata key="http://tizen.org/metadata/tizenclaw/skill"
          value="get_sample_info|get_sample_status|get_sample_time_node|get_sample_load_native|my_new_skill"/>
```

또는 별도의 메타데이터 항목으로 추가할 수도 있습니다:

```xml
<metadata key="http://tizen.org/metadata/tizenclaw/skill" value="my_new_skill"/>
```

### 6. Spec 파일 수정

`packaging/tizenclaw-skill-plugin-sample.spec`의 `%files` 섹션에 새 스킬 파일을 추가합니다:

```spec
# Python / Node.js 스킬의 경우
/usr/apps/org.tizen.tizenclaw-skill-plugin-sample/lib/my_new_skill/manifest.json
/usr/apps/org.tizen.tizenclaw-skill-plugin-sample/lib/my_new_skill/skill.py

# 네이티브 스킬의 경우 (실행 권한 설정)
/usr/apps/org.tizen.tizenclaw-skill-plugin-sample/lib/my_new_skill/manifest.json
%attr(755,root,root) /usr/apps/org.tizen.tizenclaw-skill-plugin-sample/lib/my_new_skill/my_new_skill
```

### 7. 빌드 및 배포

```bash
./deploy.sh
```

---

## 설계 가이드라인

### JSON 출력

모든 스킬은 반드시 stdout으로 **유효한 JSON**을 출력해야 합니다. 이는 LLM 파싱에 필수적입니다:

- **성공**: `{"key": "value", ...}`
- **오류**: `{"error": "설명 메시지"}`
- 항상 정확히 **한 줄**의 JSON을 출력

### 파라미터 처리

스킬은 `CLAW_ARGS` 환경 변수를 통해 JSON 문자열로 파라미터를 전달받습니다:

```python
import json, os
args = json.loads(os.environ.get("CLAW_ARGS", "{}"))
```

```javascript
const args = JSON.parse(process.env.CLAW_ARGS || '{}');
```

### manifest.json 작성 지침

`manifest.json`은 LLM이 스킬을 이해하기 위해 읽는 문서입니다. 설명은 다음과 같이 작성하세요:

- **구체적으로** — LLM에게 반환되는 데이터를 정확히 알려주기
- **행동 지향적으로** — 동사로 시작 (예: "Get", "Query", "Check")
- **문맥이 풍부하게** — 반환 형식 힌트를 설명에 포함
- **파라미터 완전하게** — 모든 파라미터에 명확한 설명과 타입 기술

### 보안

- RPK 스킬 플러그인은 반드시 **플랫폼 레벨 인증서**로 서명해야 합니다
- 배포 시 `unified-backend --preload`를 통해 등록됩니다
- 각 스킬은 제한된 시스템 접근 권한을 가진 샌드박스 환경에서 실행됩니다

---

## 빌드 아키텍처 지원

프로젝트는 여러 아키텍처를 지원합니다:

| 아키텍처 | 대상 |
|---------|------|
| `x86_64` | Tizen 에뮬레이터 |
| `armv7l` | 32비트 ARM 디바이스 |
| `aarch64` | 64비트 ARM 디바이스 |

```bash
# 특정 아키텍처로 빌드
./deploy.sh -a armv7l

# 에뮬레이터용 빌드 (기본값: sdb를 통해 자동 감지)
./deploy.sh
```
