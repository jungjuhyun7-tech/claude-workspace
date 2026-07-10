# claude-workspace

Jason의 Claude Code 작업 공간입니다.

---

## 폴더 구조

```
claude-workspace/
├── CLAUDE.md              # Claude Code 행동 지침 (메인 설정)
├── SECURITY.md            # 보안 비상 매뉴얼
├── PROGRESS.md            # 작업 진행 기록
├── .gitignore             # Git 제외 파일 목록
│
├── TASK/
│   └── TODO.md            # 현재 할 일 체크리스트
│
├── docs/
│   └── sample_sales.csv   # 샘플 데이터
│
└── weather_fetch.py       # 날씨 데이터 수집 스크립트
```

---

## 주요 파일 설명

| 파일 | 설명 |
|------|------|
| `CLAUDE.md` | Claude Code에게 주는 지침서. 보안 규칙, 소통 방식, 작업 원칙 포함 |
| `SECURITY.md` | API 키 노출 등 비상 상황 대응 매뉴얼 |
| `PROGRESS.md` | 완료된 작업 기록 (append-only) |
| `TASK/TODO.md` | 진행 중인 작업 체크리스트 |
| `weather_fetch.py` | 기상청 API 연동 날씨 수집 스크립트 |

---

## 보안 규칙

- `.env` 파일은 이 레포에 **포함되지 않습니다** (`.gitignore` 처리)
- API 키, SSH 키, 비밀번호는 환경변수로만 관리
- 민감 파일 목록: `.env`, `*.key`, `*.pem`, `credentials*`
