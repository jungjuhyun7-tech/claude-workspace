# 🚨 보안 비상 매뉴얼

> 키 노출이 의심될 때 즉시 이 파일을 열고 순서대로 따라합니다.

---

## 1단계 — 노출된 키 파악

어떤 키가 노출됐는지 먼저 확인합니다.

| 키 종류 | 확인 방법 |
|--------|---------|
| OpenRouter API 키 | `sk-or-v1-` 로 시작하는 문자열 |
| Oracle Cloud 키 | `~/.ssh/oracle-server.key` 또는 OCI API 키 |
| WordPress 비밀번호 | WordPress 관리자 계정 |
| GitHub 토큰 | `ghp_` 또는 `github_pat_` 로 시작 |
| 기타 환경변수 | `~/claude-workspace/.env` 내 변수 |

---

## 2단계 — 즉시 폐기

### OpenRouter API 키
1. [https://openrouter.ai](https://openrouter.ai) 로그인
2. Settings → API Keys → 해당 키 Delete
3. 새 키 생성

### Oracle Cloud
1. OCI 콘솔 접속
2. Identity → API Keys → 해당 키 Delete
3. 새 API 키 생성 후 `~/.oci/config` 업데이트

### GitHub 토큰
1. GitHub → Settings → Developer settings → Personal access tokens
2. 해당 토큰 Delete
3. 새 토큰 생성

---

## 3단계 — 환경변수 교체

```bash
# .env 파일 열기 (절대 공유하지 말 것)
nano ~/claude-workspace/.env

# 해당 변수를 새 키로 교체 후 저장
```

---

## 4단계 — 사용 이력 확인

### OpenRouter 사용 이력
- [https://openrouter.ai](https://openrouter.ai) → Activity 탭 확인
- 비정상적인 호출이 있으면 OpenRouter 지원팀에 신고

### Oracle 접속 이력
```bash
# Oracle 서버 접속 로그 확인
ssh oracle-server "sudo cat /var/log/auth.log | tail -50"
```

### Git 히스토리에 키가 커밋된 경우
```bash
# 민감 정보가 포함된 커밋 확인
git log --all --full-history -- .env
git log -p --all | grep "sk-or-v1-"
```

---

## 5단계 — 재발 방지

```bash
# .gitignore에 민감 파일 등록 확인
cat ~/claude-workspace/.gitignore
```

`.gitignore` 에 반드시 포함되어야 할 항목:
```
.env
*.key
*.pem
id_rsa
credentials
secrets.json
```

---

## 긴급 연락처

- **OpenRouter 지원:** support@openrouter.ai
- **Oracle Cloud 지원:** [https://support.oracle.com](https://support.oracle.com)
- **GitHub 지원:** [https://support.github.com](https://support.github.com)

---

*이 파일은 Claude Code가 보안 사고 발생 시 즉시 안내하는 매뉴얼입니다.*
