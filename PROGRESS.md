# 작업 기록

> 완료된 작업을 날짜순으로 기록합니다. 삭제 금지 (append-only).

---

## 2026-06-26

- 작업 환경 초기 구축 완료
  - `tasks/todo.md`, `tasks/progress.md` 생성
  - `SECURITY.md` 비상 매뉴얼 작성
  - `README.md` 폴더 구조 정리
  - CLAUDE.md 규칙 숙지 완료

---

## 2026-10-21

- 맥북 AI 사용량 메뉴바 앱 설치 (Pace, github.com/amitray007/pace, MIT)
  - GitHub 검색 후 후보 비교, 소스 점검: 외부 접속은 각 서비스 공식 서버뿐 (전체 코드 정독은 아님)
  - Xcode 27.1, xcodegen 2.46.0 준비 → 소스 빌드(`make install`) → `/Applications/Pace.app` 설치
  - Claude: 키체인 승인(항상 허용) 후 사용량 표시 확인됨
  - Cursor: Cursor CLI 설치·로그인 완료(사용자 보고). Pace 화면 표시는 미확인
  - Grok: 미확인 (Grok CLI 설치·로그인 필요)
  - 미확인 위험: Pace의 토큰 갱신이 Claude Code 로그인에 영향을 주는지 (현재까지 이상 보고 없음)
- CLAUDE.md의 기록 파일 경로를 실제 파일명(`TASK/TODO.md`, `PROGRESS.md`)에 맞춰 수정
- 참고: Pace를 다시 빌드할 때마다 키체인 승인을 서비스별로 다시 해야 함

- (2026-10-21 추가) 확인 완료: Pace 패널에서 Claude, Cursor, Grok 사용량 모두 정상 표시 (사용자 확인)
