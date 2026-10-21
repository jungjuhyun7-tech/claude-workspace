# 오늘 할 일

> 작업 시작 시 이 파일을 확인하고, 완료된 항목은 `[x]`로 체크합니다.
> 날짜별로 섹션을 추가해 관리합니다.

---

## 2026-06-26

- [x] tasks 폴더 및 todo.md, progress.md 생성
- [x] SECURITY.md 비상 매뉴얼 작성
- [x] README.md 폴더 구조 정리
- [ ] .env 파일 생성 및 환경변수 설정 (필요 시)

---

## 2026-10-21 — 맥북 AI 사용량 메뉴바 앱 (Pace) 설치

선정: [amitray007/pace](https://github.com/amitray007/pace) (MIT, Claude·Cursor·Grok 등 지원). 코드 점검 완료: 외부 접속은 각 서비스 공식 서버뿐.
요구사항: macOS 15 이상, Xcode(명령줄 도구만으로는 부족할 수 있음 — 모르겠어요, 빌드 시 확인 필요).

- [x] 1. 맥 버전 확인: 메뉴  > 이 Mac에 관하여 (15 이상인지)
- [x] 2. Xcode 설치 확인: 터미널에서 `xcodebuild -version`
- [x] 3. 소스 받기: `git clone https://github.com/amitray007/pace ~/pace`
- [x] 4. (선택) 설치 스크립트 직접 훑어보기: `~/pace/Scripts/install-app.sh`, `create-signing-identity.sh`
- [x] 5. 설치: `cd ~/pace && make install`
  - 하는 일: 로컬 자체서명 인증서를 로그인 키체인에 만들고 신뢰 등록 → Release 빌드 → `/Applications/Pace.app` 설치(기존 Pace.app이 있으면 교체)
- [x] 6. 실행: `open -a /Applications/Pace.app` → 메뉴바 아이콘 확인
- [x] 7. 키체인 승인: 패널의 "Allow keychain access" → 로그인 암호 입력 → **Always Allow** (Claude Code, Cursor 각각)
- [ ] 8. Grok: CLI 설치·로그인(`grok login`) 후 Pace에서 `Add current Grok account` — 미확인
- [ ] 9. 확인 후 이 목록 체크, `PROGRESS.md`에 결과 기록

주의
- 업데이트(새로 빌드)할 때마다 키체인 승인을 다시 해야 함 (서명 없는 앱의 macOS 규칙).
- Cursor·Claude·Grok의 비공식 주소를 쓰므로 서비스 쪽 변경 시 갑자기 안 될 수 있음.
- Claude Code 토큰 갱신에 영향을 주는지는 미확인 — 설치 후 Claude Code 로그인이 풀리면 중단하고 알려주기.
- 에러가 나면 다음 단계로 가지 말고 에러 메시지를 그대로 전달.

---

## 사용법

새 작업 추가 방법:
```
## YYYY-MM-DD
- [ ] 할 일 내용
```

완료 시:
```
- [x] 완료된 내용
```
