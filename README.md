# 🚗 자동차 스프링 업계 뉴스 자동화 리포트 시스템

매일 아침 8시에 자동차 스프링 관련 국내외 뉴스를 자동으로 수집하여 분석하고, 전문적인 HTML 리포트를 생성하는 자동화 시스템입니다.

## 📋 기능

- ✅ **자동 뉴스 수집**: 매일 아침 8시 자동 실행
- ✅ **AI 분석**: Claude API를 사용한 전문적 요약
- ✅ **자동 이슈 추출**: 주요 이슈 5개 자동 식별
- ✅ **HTML 리포트**: 깔끔한 전문가 수준의 리포트
- ✅ **한글 완전 지원**: 모든 콘텐츠가 한글로 표시
- ✅ **원문 링크 포함**: 각 뉴스의 원문으로 바로 이동 가능

## 🚀 빠른 시작

### 1단계: Python 설치

**Windows에서 Python 설치 방법:**

1. https://www.python.org/downloads/ 방문
2. "Download Python 3.12" (또는 최신 버전) 클릭
3. 설치 파일 실행
4. **중요**: "Add Python to PATH" 체크 ✓
5. "Install Now" 클릭

**설치 확인:**
```bash
python --version
```

### 2단계: 가상환경 생성

프로젝트 폴더에서 다음 명령어를 실행하세요:

```bash
# Windows PowerShell
python -m venv venv
venv\Scripts\activate

# 또는 Command Prompt
python -m venv venv
venv\Scripts\activate.bat
```

**가상환경 활성화 확인:**
- 터미널 왼쪽에 `(venv)`가 표시되면 정상입니다.

### 3단계: 의존성 설치

```bash
pip install -r requirements.txt
```

**설치 완료 시:**
```
Successfully installed APScheduler anthropic beautifulsoup4 ...
```

### 4단계: API 키 설정

1. https://console.anthropic.com 방문
2. 로그인 또는 가입
3. "API Keys" 메뉴에서 "Create Key" 클릭
4. API 키 복사

`.env` 파일을 열고 다음과 같이 수정:

```env
ANTHROPIC_API_KEY=sk-ant-v0-xxxxxxxxxxxxxxxxxxxx
```

**⚠️ 중요**: API 키는 절대 공개하지 마세요!

### 5단계: 프로그램 실행

```bash
python main.py
```

**정상 실행 시 표시:**
```
============================================================
✅ 시스템이 준비되었습니다!
============================================================
📅 실행 시간: 매일 08:00
📁 리포트 저장 경로: C:\Users\...\spring_news_automation\output\reports
```

## 📁 생성되는 리포트 위치

```
spring_news_automation/
└── output/
    └── reports/
        └── 2026-06-11/
            └── report.html    ← 이 파일을 브라우저에서 열어 보세요!
```

**리포트 보기:**
1. 생성된 `report.html` 파일 찾기
2. 파일을 마우스 우클릭
3. "다른 프로그램으로 열기" → "Chrome" 또는 "Edge"
4. 또는 `report.html`을 직접 더블클릭

## 💡 사용 예시

### 아침에 자동 실행되는 방식

매일 아침 8시가 되면 다음이 자동으로 실행됩니다:

```
08:00:00 - [1/3] 뉴스 수집 중...
08:00:15 - ✓ 10개의 뉴스 수집 완료
08:00:16 - [2/3] Claude AI로 뉴스 분석 중...
08:00:35 - ✓ 분석 완료: 10개 요약, 5개 이슈, 12개 키워드
08:00:36 - [3/3] HTML 리포트 생성 중...
08:00:37 - ✓ 리포트 생성 완료: output/reports/2026-06-11/report.html
08:00:37 - ✅ 모든 작업이 정상적으로 완료되었습니다.
```

### PC 절전 모드 관련 주의사항

⚠️ **자동 실행을 위해 PC 절전 모드를 비활성화해야 합니다:**

1. Windows 설정 열기
2. "전원 및 절전" → "전원 계획"
3. "고성능" 선택 또는 절전 시간 길게 설정

## 🔧 트러블슈팅

### 문제: "command not found: python"
**해결:** Python을 다시 설치하고 PATH에 추가했는지 확인하세요.

### 문제: "No module named 'anthropic'"
**해결:** `pip install -r requirements.txt`를 다시 실행하세요.

### 문제: "ANTHROPIC_API_KEY not found"
**해결:** `.env` 파일에서 API 키가 올바르게 설정되었는지 확인하세요.

### 문제: 프로그램이 8시에 실행되지 않음
**해결:** 
1. 컴퓨터 시간이 정확한지 확인
2. PC 절전 모드 비활성화
3. 방화벽이 차단하지 않는지 확인

## 📊 리포트 구성

생성되는 HTML 리포트는 다음과 같이 구성됩니다:

```
┌─────────────────────────────────────────┐
│  자동차 스프링 업계 뉴스 리포트           │
│  2026년 6월 11일 (목요일)               │
├─────────────────────────────────────────┤
│ ⚠️  오늘의 주요 이슈 (상위 5개)          │
│     • 이슈 1: ...                       │
│     • 이슈 2: ...                       │
│     ...                                 │
├─────────────────────────────────────────┤
│ 📰 상세 뉴스 분석 (10개)                │
│   [1] 뉴스 제목 1                       │
│       출처 | 시간                       │
│       [한글 요약]                       │
│       영향도: 높음                      │
│       [원문 보기]                       │
│                                         │
│   [2] 뉴스 제목 2                       │
│       ...                               │
├─────────────────────────────────────────┤
│ 🏷️  주요 키워드                         │
│     #전동차 #스프링 #경량화 ...        │
└─────────────────────────────────────────┘
```

## 🎯 고급 설정

### 실행 시간 변경

`config.py`의 다음 부분을 수정:

```python
SCHEDULER = {
    "hour": 8,      # 시간 (0-23)
    "minute": 0,    # 분 (0-59)
    "timezone": "Asia/Seoul",
}
```

예: 오후 2시에 실행하려면 `"hour": 14`

### 수집 뉴스 개수 변경

`config.py`의 다음 부분을 수정:

```python
NEWS_COLLECTION = {
    "max_articles": 10,  # 10 → 15로 변경하면 15개 수집
}
```

## 📝 로그 확인

프로그램의 실행 기록은 다음 위치에 저장됩니다:

```
spring_news_automation/
└── logs/
    ├── spring_news_automation_latest.log
    └── ...
```

## ⚙️ 시스템 요구사항

- **OS**: Windows 10 이상
- **Python**: 3.9 이상
- **인터넷**: 필수 (뉴스 수집용)
- **API 키**: Anthropic API 키 필수

## 🆘 도움말

### 가상환경이란?
파이썬 프로젝트마다 독립적인 환경을 만드는 것입니다. 다른 프로젝트와 라이브러리 버전이 충돌하지 않도록 합니다.

### API 키는 어디서 얻나요?
1. https://console.anthropic.com 방문
2. "API Keys" 탭에서 "Create Key" 클릭
3. 발급받은 키를 `.env` 파일에 입력

### 매일 실행되나요?
네! `APScheduler`가 매일 설정된 시간에 자동으로 실행합니다. PC가 켜져있어야 합니다.

### 리포트를 이메일로 받을 수 있나요?
현재는 로컬 폴더에 저장됩니다. 향후 이메일 발송 기능을 추가할 수 있습니다.

## 📞 문제 해결

**프로그램이 자꾸 종료된다면:**
```bash
# 로그를 확인해보세요
cat logs/spring_news_automation_latest.log
```

**API 키 오류가 발생한다면:**
1. `.env` 파일이 프로젝트 폴더에 있는지 확인
2. API 키가 정확하게 복사되었는지 확인
3. API 키에 공백이 없는지 확인

## 📚 더 알아보기

- [Anthropic Claude API 문서](https://docs.anthropic.com)
- [APScheduler 문서](https://apscheduler.readthedocs.io)
- [BeautifulSoup 문서](https://www.crummy.com/software/BeautifulSoup)

---

**버전**: 1.0.0  
**마지막 업데이트**: 2026-06-11  
**개발자**: Claude Code AI Assistant

행운을 빕니다! 🎉
