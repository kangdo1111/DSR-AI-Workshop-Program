# CLAUDE.md - 프로젝트 컨텍스트

## 프로젝트 상황

**자동차 스프링 업계 뉴스 자동화 시스템**
- 상태: v1 완성 (스킬 구현 완료)
- 타입: Python 자동화 + Claude AI + GitHub automation
- 사용자: 20년차 자동차 부품 스프링 업계 전문가

---

## 핵심 기능

### 뉴스 자동화 (main.py)
```
매일 8시 → 뉴스 수집 → AI 분석 → HTML 리포트 생성
```

**수집**: RSS 피드 (Google News, 네이버, 뉴스와이어)
**분석**: Claude 3.5 Sonnet (전문 요약, 이슈 추출)
**저장**: `output/reports/YYYY-MM-DD/report.html`

### 이슈 관리 (스킬)
- `/issue-writer`: 산출물 검증 → 이슈 생성
- `/issue-runner`: 이슈 분석 → 코드 수정 → 커밋

---

## 파일 구조

```
spring_news_automation/
├── main.py                 # 메인 실행 파일
├── config.py              # 설정 (뉴스 소스, API, 스케줄)
├── requirements.txt       # Python 의존성
├── .env                   # API 키 (Anthropic)
│
├── modules/
│   ├── news_collector.py  # RSS 수집 + 필터 (날짜, 중복, 관련성)
│   ├── ai_analyzer.py     # Claude AI 분석
│   ├── report_generator.py # HTML 생성
│   └── scheduler.py       # APScheduler (8시 실행)
│
├── templates/
│   └── report_template.html # Jinja2 템플릿
│
├── output/reports/        # 생성된 리포트
├── logs/                  # 실행 로그
├── data/                  # 캐시 DB
│
├── ISSUES.md              # 8개 이슈 (4완료, 4예정)
├── SKILL.md               # 프로젝트 스킬
├── CLAUDE.md              # 이 파일
├── SOUL.md                # 프로젝트 영혼
└── README.md              # 사용자 가이드
```

---

## 에이전트 팀 (Managed Agents)

### 팀 구조
```
📋 메인 뉴스 분석기 (조정자)
├── 🔍 보안 검증 에이전트 (전문가)
├── ⚡ 성능 분석 에이전트 (전문가)
└── ✅ 콘텐츠 검증 에이전트 (전문가)
```

### 팀 역할
- **메인 뉴스 분석기 (조정자)**: 뉴스 수집 → 분석 흐름 관리, 전문가들에게 작업 위임
- **보안 검증 에이전트**: RSS 피드 URL 검증, 데이터 무결성 확인
- **성능 분석 에이전트**: 수집 속도, AI 응답 시간 분석
- **콘텐츠 검증 에이전트**: 뉴스 관련성, 요약 품질 검증

### 활성화
- 각 에이전트는 독립적 컨텍스트 유지
- 공유 파일시스템 (`/workspace/data`) 활용
- 병렬 처리로 전체 분석 시간 단축

## 주요 결정사항

### v0 → v1 진화
- **v0**: 수동 검증 → ISSUES.md 작성 → 코드 수정
- **v1**: 스킬 자동화 → `/issue-writer` → `/issue-runner`

### 필터링 알고리즘
1. **날짜**: 최근 7일만
2. **중복**: 유사도 80% 이상 제외 (제목+요약)
3. **관련성**: 스프링 키워드 필터 + 제외 키워드

### 이슈 상태
| # | 상태 | 커밋 |
|---|------|------|
| 1-4 | ✅ 완료 | 039dd39 |
| 5-8 | ⏳ 예정 | - |

---

## 중요 설정

### config.py
```python
SCHEDULER = {
    "hour": 8,              # 매일 8시
    "timezone": "Asia/Seoul",
}

NEWS_COLLECTION = {
    "max_articles": 10,     # 뉴스 10개
}

AI_ANALYSIS = {
    "model": "claude-3-5-sonnet-20241022",
    "max_tokens": 2000,
}
```

### .env (필수)
```
ANTHROPIC_API_KEY=sk-ant-xxxxx
```

---

## 개발 노트

### news_collector.py 개선사항
- `collect_from_sources()`: Google News 2개 URL 추가
- `remove_duplicates()`: SequenceMatcher로 유사도 계산
- `filter_by_relevance()`: 스프링 키워드 + 제외 키워드
- `filter_by_date()`: parsedate_to_datetime으로 날짜 검증

### ai_analyzer.py 상태
- Claude API 연동 가능 (API 키 있을 때)
- 폴백: 로컬 테스트 데이터 (API 키 없을 때)

### main.py 수정
- `daily_task()`: collect_news() 호출 추가
- 뉴스 없을 시 경고 + 로그 기록

---

## 다음 작업 (Issue #5-8)

### #5: 통계 출처 검증
- ai_analyzer.py에 `[출처: OOO]` 형식 추가
- 출처 없는 수치에 ⚠️ 표시

### #6: 링크 유효성 검증
- news_collector.py URL 검증 함수
- 404/연결 실패 URL 제외

### #7: 리포트 범위 명시
- report_template.html 헤더 수정
- "금주 종합 (2026.06.07~06.13)" 형식

### #8: 이슈 우선순위 재평가
- 뉴스 빈도 기반 이슈 추출
- 같은 테마 3개 이상만 이슈로 인정

---

## 주의사항

⚠️ **PC 상태**:
- 절전 모드 비활성화 필수
- 프로그램 24시간 실행 필요 (8시에 자동 실행)

⚠️ **API 키**:
- .env 파일에만 저장
- 절대 GitHub에 커밋 금지

⚠️ **네트워크**:
- RSS 피드 연결 필수
- 타임아웃 30초 설정

---

**작성**: Claude Code AI Assistant  
**마지막 업데이트**: 2026-06-11  
**버전**: v1.0
