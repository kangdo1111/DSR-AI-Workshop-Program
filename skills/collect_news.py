"""
collect-news 스킬: RSS 피드 수집 및 필터링

Collector Agent가 사용하는 메인 스킬입니다.
RSS 피드에서 뉴스를 수집하고 필터링합니다.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
import hashlib
from difflib import SequenceMatcher
import feedparser
from typing import Optional


class NewsCollector:
    """RSS 피드 수집 및 필터링"""

    NEWS_SOURCES = {
        "google_news_spring": [
            "https://news.google.com/rss/search?q=자동차+스프링&hl=ko&gl=KR&ceid=KR:ko",
            "https://news.google.com/rss/search?q=suspension+spring&hl=en&gl=US&ceid=US:en"
        ],
        "naver_news": [
            "https://news.naver.com/rss/section/105.xml"  # 자동차
        ],
        "newswire": [
            "https://www.newswire.co.kr/newswire/categoryRssView.php?cat_cd=c1006"  # 자동차
        ]
    }

    SPRING_KEYWORDS = [
        "스프링", "spring", "현가", "suspension", "샤시", "chassis",
        "코일", "leaf spring", "판스프링", "탄성", "댐핑",
        "NVH", "진동", "완충", "쇼바", "strut"
    ]

    EXCLUDE_KEYWORDS = [
        "벚꽃", "봄", "스프링쿨", "매직스프링", "워터스프링",
        "스프링데이", "스프링타임"
    ]

    def __init__(self):
        self.workspace_dir = Path("/workspace/data")
        self.workspace_dir.mkdir(parents=True, exist_ok=True)

    def collect_from_sources(self) -> list[dict]:
        """RSS 피드에서 뉴스 수집"""
        articles = []

        for source_name, urls in self.NEWS_SOURCES.items():
            for url in urls:
                try:
                    feed = feedparser.parse(url)
                    for entry in feed.entries[:10]:
                        article = {
                            "title": entry.get("title", ""),
                            "url": entry.get("link", ""),
                            "content": entry.get("summary", ""),
                            "source": source_name,
                            "date": entry.get("published", datetime.now().isoformat())
                        }
                        articles.append(article)
                except Exception as e:
                    print(f"Error fetching {url}: {e}")

        return articles

    def filter_by_date(self, articles: list[dict], days: int = 7) -> list[dict]:
        """최근 N일 뉴스만 필터링"""
        cutoff_date = datetime.now() - timedelta(days=days)
        filtered = []

        for article in articles:
            try:
                pub_date = datetime.fromisoformat(article["date"].replace("Z", "+00:00"))
                if pub_date >= cutoff_date:
                    filtered.append(article)
            except:
                filtered.append(article)  # 날짜 파싱 실패하면 포함

        return filtered

    def remove_duplicates(self, articles: list[dict], threshold: float = 0.8) -> list[dict]:
        """제목+요약 기반 중복 제거"""
        unique_articles = []
        seen_hashes = set()

        for article in articles:
            text = (article.get("title", "") + " " + article.get("content", "")).lower()

            is_duplicate = False
            for existing_article in unique_articles:
                existing_text = (
                    existing_article.get("title", "") + " " + existing_article.get("content", "")
                ).lower()

                similarity = SequenceMatcher(None, text, existing_text).ratio()
                if similarity >= threshold:
                    is_duplicate = True
                    break

            if not is_duplicate:
                unique_articles.append(article)

        return unique_articles

    def filter_by_relevance(self, articles: list[dict]) -> list[dict]:
        """스프링 업계 관련성 필터링"""
        relevant_articles = []

        for article in articles:
            text = (
                article.get("title", "") + " " + article.get("content", "")
            ).lower()

            # 제외 키워드 확인
            if any(keyword.lower() in text for keyword in self.EXCLUDE_KEYWORDS):
                continue

            # 포함 키워드 확인
            if any(keyword.lower() in text for keyword in self.SPRING_KEYWORDS):
                relevant_articles.append(article)

        return relevant_articles

    def collect(self, max_articles: int = 10) -> dict:
        """전체 수집 파이프라인"""
        print("[Collector] RSS 피드에서 뉴스 수집 중...")
        articles = self.collect_from_sources()
        print(f"[Collector] {len(articles)}개 뉴스 수집됨")

        articles = self.filter_by_date(articles, days=7)
        print(f"[Collector] 필터링 후: {len(articles)}개")

        articles = self.remove_duplicates(articles, threshold=0.8)
        print(f"[Collector] 중복 제거 후: {len(articles)}개")

        articles = self.filter_by_relevance(articles)
        print(f"[Collector] 관련성 필터링 후: {len(articles)}개")

        articles = articles[:max_articles]

        result = {
            "timestamp": datetime.now().isoformat(),
            "total_count": len(articles),
            "articles": articles
        }

        # 결과 저장
        output_file = self.workspace_dir / "collected_news.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"[Collector] 결과 저장: {output_file}")
        return result


def run_skill() -> dict:
    """스킬 실행"""
    collector = NewsCollector()
    return collector.collect(max_articles=10)


if __name__ == "__main__":
    result = run_skill()
    print("\n=== 수집 결과 ===")
    print(json.dumps(result, ensure_ascii=False, indent=2))
