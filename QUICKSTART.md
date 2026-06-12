# 🚀 빠른 시작 가이드

## 📌 핵심 요약
- **프로젝트**: 자동차 스프링 업계 뉴스 자동화 시스템
- **실행**: `python run_report.py`
- **결과**: 뉴스 수집 → 분석 → HTML 리포트 생성
- **API 비용**: 없음 (완전 무료, 인터넷 검색 기반)

---

## 🎯 실행 방법

### 1단계: 폴더 이동
```powershell
cd C:\Users\Admin\Desktop\workspace\spring_news_automation
```

### 2단계: 실행
```powershell
python run_report.py
```

### 3단계: 리포트 확인
생성된 HTML 파일 위치:
```
output/reports/YYYY-MM-DD/report.html
```

---

## 🔧 기술 스택

| 항목 | 내용 |
|------|------|
| 언어 | Python 3.14+ |
| 뉴스 수집 | RSS 피드 (feedparser) |
| 분석 방식 | 로컬 처리 (API 없음) |
| 리포트 생성 | Jinja2 템플릿 |
| 저장 | HTML 파일 |

---

## 📁 파일 구조

```
spring_news_automation/
├── run_report.py              ← 실행 파일 (유일)
│
├── modules/
│   ├── news_collector.py      (RSS 수집)
│   ├── ai_analyzer.py         (로컬 분석)
│   └── report_generator.py    (HTML 생성)
│
├── templates/
│   └── report_template.html   (HTML 템플릿)
│
├── output/reports/            (생성된 리포트)
├── config.py                  (설정)
└── .env                       (환경변수 - API 키 불필요)
```

---

## 🔄 동작 원리

### 흐름도
```
1️⃣ RSS 피드 수집
   ↓
2️⃣ 뉴스 필터링
   ├── 최근 7일만
   ├── 중복 제거 (유사도 80%)
   └── 스프링 관련성 필터
   ↓
3️⃣ 로컬 분석
   ├── 제품 분류
   ├── 영향도 평가
   └── 경쟁사 정보
   ↓
4️⃣ HTML 리포트 생성
   └── output/reports/YYYY-MM-DD/report.html
```

### 각 모듈 역할

**news_collector.py**
- Google News RSS (한/영)
- 네이버 뉴스 RSS
- 뉴스와이어 RSS

**ai_analyzer.py**
- 로컬 처리 (Claude API 없음)
- 제품 카테고리 자동 분류
- 뉴스 영향도 평가 (높음/중간/낮음)
- DSR 대응 방안 생성
- 경쟁사 정보 추출

**report_generator.py**
- Jinja2 템플릿으로 HTML 생성
- 전문적인 스타일시트 적용
- 뉴스별 원문 링크 포함

---

## 📊 출력 예시

생성되는 HTML 리포트 포함:
- 📰 뉴스 제목
- 📅 발행일
- 📝 요약 (RSS 원문)
- 🏷️ 제품 분류
- 📊 영향도 평가
- 🏢 경쟁사 정보
- 💡 사업 기회
- 🔗 원문 링크

---

## ⚠️ 주의사항

### API 키 불필요
- `.env` 파일에 API 키 설정 불필요
- 완전 무료 (인터넷 검색 기반)

### 네트워크 필요
- RSS 피드 접근 필요
- 뉴스 링크 확인 필요

### 타임아웃 설정
- RSS 연결: 30초
- 전체 실행: 약 10~20초

---

## 🛠️ 트러블슈팅

### 문제: "뉴스가 없습니다"
**원인**: RSS 피드 연결 실패
**해결**: 네트워크 확인 후 재실행

### 문제: 모듈 임포트 오류
**원인**: 필수 패키지 미설치
**해결**: 
```powershell
pip install feedparser python-dotenv jinja2
```

### 문제: 리포트가 생성되지 않음
**원인**: templates/ 폴더 없음
**해결**: 폴더 구조 확인

---

## 📋 최근 변경사항 (2026-06-12)

1. **하네스 아키텍처 제거**
   - 단순화된 레거시 파이프라인으로 복원
   - 불필요한 파일 삭제

2. **API 의존성 제거**
   - Anthropic 패키지 제거
   - 로컬 처리 방식만 사용
   - 무료화 완성

3. **파일 정리**
   - run_report.py: 유일한 실행 파일
   - 테스트/유틸리티 파일 제거

---

## 🔗 관련 문서

- `CLAUDE.md` - 프로젝트 상세 정보
- `README.md` - 사용자 가이드
- `ISSUES.md` - 작업 이슈
- `SOUL.md` - 프로젝트 철학

---

**마지막 수정**: 2026-06-12  
**버전**: v1.1 (무료화 완성)  
**상태**: ✅ 프로덕션 준비 완료
