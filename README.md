# 🚗 자동차 스프링 업계 뉴스 자동화 시스템

매일 아침 8시에 자동으로 자동차 스프링 관련 뉴스를 수집하여 분석하고 전문가 수준의 HTML 리포트를 생성합니다.

---

## ✨ 주요 기능

- 📰 **자동 뉴스 수집**: 매일 아침 8시에 RSS 피드에서 최신 뉴스 10개 자동 수집
- 🤖 **AI 전문 분석**: Claude를 활용한 한글 요약 및 영향도 평가
- ⚠️ **주요 이슈 추출**: 자동으로 5개의 주요 이슈 식별
- 🎨 **전문 리포트**: 깔끔한 HTML 형식의 일일 리포트 생성
- 🔄 **자동 필터링**: 날짜, 중복, 관련성을 자동으로 검증

---

## 🚀 빠른 시작 (5분)

### 1단계: 설치
```bash
# 저장소 클론
git clone https://github.com/kangdo1111/DSR-AI-Workshop-Program.git
cd DSR-AI-Workshop-Program/spring_news_automation

# Python 환경 설정
python -m venv venv
venv\Scripts\activate  # Windows

# 라이브러리 설치
pip install -r requirements.txt
```

### 2단계: API 키 설정
```bash
# .env 파일 수정
ANTHROPIC_API_KEY=sk-ant-YOUR_KEY_HERE
```

**API 키 발급**: https://console.anthropic.com

### 3단계: 실행
```bash
python main.py
```

**리포트 확인**: `output/reports/YYYY-MM-DD/report.html`

---

## 📋 리포트 구성

생성되는 HTML 리포트에는 다음이 포함됩니다:

```
┌─────────────────────────────────┐
│ 자동차 스프링 업계 뉴스 리포트   │
│ 2026년 6월 11일 (목요일)        │
├─────────────────────────────────┤
│ ⚠️ 오늘의 주요 이슈 (5개)       │
│   1. 전동화 전환 추진           │
│   2. 경량화 기술 강화           │
│   3. 공급망 안정화             │
│   ...                          │
├─────────────────────────────────┤
│ 📰 상세 뉴스 분석 (10개)        │
│   [1] 제목                      │
│        출처 | 시간              │
│        한글 요약...             │
│        영향도: 높음             │
│        [원문 보기]              │
│   [2] ...                       │
├─────────────────────────────────┤
│ 🏷️ 주요 키워드                  │
│   #전동차 #스프링 #경량화 ...   │
└─────────────────────────────────┘
```

---

## 🔧 설정 (config.py)

### 실행 시간 변경
```python
SCHEDULER = {
    "hour": 8,      # 8시 → 14로 바꾸면 오후 2시
    "minute": 0,
}
```

### 뉴스 개수 변경
```python
NEWS_COLLECTION = {
    "max_articles": 10,  # 10 → 15로 바꾸면 15개 수집
}
```

### API 모델 변경
```python
AI_ANALYSIS = {
    "model": "claude-3-5-sonnet-20241022",  # Claude 모델
    "max_tokens": 2000,
}
```

---

## 📁 파일 구조

```
spring_news_automation/
├── main.py                    # 메인 실행 파일
├── config.py                  # 설정
├── requirements.txt           # Python 의존성
├── .env                       # API 키 (절대 공개 금지!)
│
├── modules/
│   ├── news_collector.py      # RSS 뉴스 수집
│   ├── ai_analyzer.py         # Claude AI 분석
│   ├── report_generator.py    # HTML 리포트 생성
│   └── scheduler.py           # 자동 스케줄링
│
├── templates/
│   └── report_template.html   # 리포트 템플릿
│
├── output/reports/            # 생성된 리포트 저장
│   └── 2026-06-11/
│       └── report.html
│
├── logs/                      # 실행 로그
├── data/                      # 캐시 데이터
│
├── ISSUES.md                  # 이슈 추적
├── CLAUDE.md                  # 기술 문서
├── SOUL.md                    # 프로젝트 목표
└── README.md                  # 이 파일
```

---

## 🎯 사용 방법

### 자동 실행 (권장)
```bash
python main.py
# 매일 아침 8시에 자동 실행
# Ctrl+C로 중지 가능
```

### 수동 실행 (테스트)
```bash
python -c "from main import daily_task; daily_task()"
# 즉시 리포트 생성
```

### 스킬로 사용 (자동화)
```
/issue-writer    → 산출물 검증, 이슈 생성
/issue-runner    → 이슈 분석, 코드 수정, 커밋
```

---

## 📊 예상 동작

### 매일 아침 8시 자동 실행
```
08:00 시작
  ├─ 뉴스 수집 (5초)
  │  └─ 시도: 4개 소스, 성공: 3개
  ├─ AI 분석 (20초)
  │  └─ 10개 요약, 5개 이슈, 12개 키워드
  ├─ HTML 생성 (1초)
  │  └─ output/reports/2026-06-11/report.html
  └─ 완료 ✅

총 소요: 약 30초
```

---

## ⚠️ 주의사항

### PC 설정
- **절전 모드 비활성화** (8시 자동 실행을 위해)
- **프로그램 24시간 실행** (main.py 계속 실행)
- **인터넷 연결 필수** (뉴스 피드 수집)

### 보안
- **.env 파일은 절대 공개 금지** (API 키 포함)
- **GitHub에 API 키 커밋 금지**
- **개인 컴퓨터에서만 실행** (크레덴셜 노출 위험)

### 문제 해결

| 증상 | 원인 | 해결 |
|------|------|------|
| "뉴스 수집 실패" | RSS 피드 연결 문제 | 인터넷 연결 확인 |
| "API 키 오류" | .env 파일 설정 오류 | `.env` 파일의 API 키 확인 |
| "8시에 실행 안 됨" | PC 절전 모드 | Windows 절전 설정 비활성화 |
| "모듈 오류" | 라이브러리 미설치 | `pip install -r requirements.txt` 재실행 |

---

## 🔍 리포트 확인 위치

### 파일 위치
```
C:\Users\[username]\Desktop\workspace\spring_news_automation\output\reports\
```

### 날짜별 폴더
```
output/reports/
├── 2026-06-11/
│   └── report.html    ← 클릭해서 브라우저에서 열기
├── 2026-06-10/
│   └── report.html
└── ...
```

### 브라우저에서 열기
1. 폴더에서 `report.html` 찾기
2. 더블클릭 또는 우클릭 → "다른 프로그램으로 열기" → Chrome/Edge
3. 자동으로 브라우저에서 열림

---

## 🛠️ 기술 스택

- **언어**: Python 3.9+
- **뉴스 수집**: feedparser, BeautifulSoup4, requests
- **AI**: Anthropic Claude API (claude-3-5-sonnet)
- **리포트**: Jinja2 (HTML 템플릿)
- **자동화**: APScheduler (일정 관리)
- **형상**: Git + GitHub

---

## 📞 더 알아보기

- **기술 문서**: [CLAUDE.md](CLAUDE.md)
- **프로젝트 목표**: [SOUL.md](SOUL.md)
- **이슈 추적**: [ISSUES.md](ISSUES.md)
- **GitHub**: https://github.com/kangdo1111/DSR-AI-Workshop-Program

---

## 📈 프로젝트 상태

| 항목 | 상태 |
|------|------|
| 뉴스 수집 | ✅ 완성 |
| AI 분석 | ✅ 완성 |
| HTML 리포트 | ✅ 완성 |
| 자동 스케줄링 | ✅ 완성 |
| 스킬 자동화 | ✅ 완성 |
| 문서화 | ✅ 완성 |
| **전체** | **✅ v1.0 완성** |

---

**시작**: 2026-06-11  
**버전**: 1.0.0 ✅  
**상태**: 프로덕션 준비 완료
