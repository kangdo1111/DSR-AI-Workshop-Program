# ⚙️ 설치 및 설정 가이드

## 📦 필수 요구사항

- **Python**: 3.10+ (3.14 권장)
- **OS**: Windows/Mac/Linux
- **네트워크**: RSS 피드 접근 가능

## 🚀 설치 단계

### 1단계: 저장소 클론
```powershell
git clone https://github.com/kangdo1111/DSR-AI-Workshop-Program.git
cd spring_news_automation
```

### 2단계: 패키지 설치
```powershell
pip install feedparser python-dotenv jinja2
```

**설치되는 패키지**:
- `feedparser`: RSS 피드 파싱
- `python-dotenv`: 환경변수 로드
- `jinja2`: HTML 템플릿 렌더링

### 3단계: 설정 확인
**.env 파일**:
```
ANTHROPIC_API_KEY=your_api_key_here  (불필요 - 무시해도 됨)
USE_HARNESS=false                    (기본값)
```

**변경 필요 없음** - 기본값 그대로 사용 가능

### 4단계: 실행
```powershell
python run_report.py
```

---

## ✅ 정상 설치 확인

### 명령어
```powershell
python -c "import feedparser, jinja2; print('OK')"
```

### 예상 출력
```
OK
```

### 리포트 생성 확인
```powershell
python run_report.py
```

**성공 메시지**:
```
[시간] ✅ 리포트 생성 완료!
[시간] 📍 리포트 경로: output/reports/YYYY-MM-DD/report.html
```

---

## 🔧 설정 항목

### config.py
```python
SCHEDULER = {
    "hour": 8,              # 매일 8시 실행 (기본)
    "minute": 0,
    "timezone": "Asia/Seoul",
}

NEWS_COLLECTION = {
    "max_articles": 10,     # 수집 뉴스 개수
}

LOGGING = {
    "level": "INFO",
    "format": "[%(asctime)s] %(message)s",
}
```

### .env
```
# API 키 (필요 없음)
ANTHROPIC_API_KEY=your_api_key_here

# 하네스 설정 (기본값 유지)
USE_HARNESS=false

# 기타 (수정 불필요)
WORKSPACE_DIR=/workspace/data
MAX_ARTICLES=10
```

---

## 🐛 문제 해결

### 문제: "ModuleNotFoundError: No module named 'feedparser'"

**원인**: 패키지 미설치
**해결**:
```powershell
pip install feedparser python-dotenv jinja2
```

---

### 문제: "뉴스가 없습니다"

**원인**: RSS 피드 연결 실패
**확인**:
```powershell
python -c "import feedparser; f=feedparser.parse('https://news.google.com/rss/search?q=spring'); print(len(f.entries))"
```
**해결**: 네트워크 확인 후 재실행

---

### 문제: "output 폴더가 없음"

**원인**: 폴더 구조 불완전
**해결**:
```powershell
mkdir output/reports
python run_report.py
```

---

### 문제: "templates/report_template.html 없음"

**원인**: 파일 손실
**해결**: GitHub에서 다시 클론
```powershell
git checkout templates/report_template.html
```

---

## 📊 환경 정보 확인

### Python 버전
```powershell
python --version
```

### 설치된 패키지
```powershell
pip list | grep -E "feedparser|jinja2|python-dotenv"
```

### 현재 작업 폴더
```powershell
pwd
ls  # 또는 dir (Windows)
```

---

## 🔄 업데이트

### 최신 버전 가져오기
```powershell
git pull origin main
```

### 변경 사항 확인
```powershell
git log --oneline -5
```

---

## 📝 로그 확인

### 최신 로그 파일
```
logs/spring_news_automation_latest.log
```

### 로그 확인 명령어
```powershell
tail -50 logs/spring_news_automation_latest.log
```

---

## ✨ 완성!

설치가 완료되었습니다. 이제 다음 명령어로 실행하세요:

```powershell
python run_report.py
```

자세한 사용법은 **QUICKSTART.md** 참조

---

**버전**: v1.1  
**마지막 업데이트**: 2026-06-12  
**문의**: GitHub Issues
