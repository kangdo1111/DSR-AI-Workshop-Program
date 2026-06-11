"""
설정 파일 - 뉴스 자동화 시스템의 모든 설정을 관리합니다.
"""
import os
from pathlib import Path

# 프로젝트 루트 디렉토리
PROJECT_ROOT = Path(__file__).parent

# 뉴스 관련 설정
NEWS_SOURCES = {
    "naver": {
        "url": "https://rss.naver.com/",
        "category": "IT",
    },
    "google_news": {
        "url": "https://news.google.com/rss/search?q=자동차+스프링",
    },
    "news_wire": {
        "url": "https://www.newswire.co.kr/newswire/rss/category_it.xml",
    },
}

# 뉴스 수집 설정
NEWS_COLLECTION = {
    "max_articles": 10,  # 수집할 최대 뉴스 수
    "timeout": 30,  # 요청 타임아웃 (초)
    "retry_count": 3,  # 재시도 횟수
}

# 리포트 생성 설정
REPORT = {
    "max_issues": 5,  # 추출할 최대 이슈 수
    "language": "ko",  # 언어 설정
    "timezone": "Asia/Seoul",  # 시간대
}

# AI 분석 설정
AI_ANALYSIS = {
    "model": "claude-3-5-sonnet-20241022",  # Claude 모델
    "max_tokens": 2000,
    "temperature": 0.7,
}

# 경로 설정
PATHS = {
    "output": PROJECT_ROOT / "output" / "reports",
    "logs": PROJECT_ROOT / "logs",
    "data": PROJECT_ROOT / "data",
    "templates": PROJECT_ROOT / "templates",
    "modules": PROJECT_ROOT / "modules",
}

# 로깅 설정
LOGGING = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "date_format": "%Y-%m-%d %H:%M:%S",
}

# 스케줄러 설정
SCHEDULER = {
    "hour": 8,  # 매일 8시
    "minute": 0,
    "timezone": "Asia/Seoul",
}

# 모든 필수 디렉토리 생성
for path in PATHS.values():
    path.mkdir(parents=True, exist_ok=True)
