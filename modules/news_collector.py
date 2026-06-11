"""
뉴스 수집 모듈 - RSS 피드에서 자동차 스프링 관련 뉴스를 수집합니다.
"""
import feedparser
import requests
import logging
from datetime import datetime
from typing import List, Dict
from bs4 import BeautifulSoup
import sys
import os

# config.py 경로 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

logger = logging.getLogger(__name__)


class NewsCollector:
    """뉴스 수집 클래스"""

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        self.collected_news = []

    def collect_from_rss(self, feed_url: str) -> List[Dict]:
        """
        RSS 피드에서 뉴스를 수집합니다.

        Args:
            feed_url: RSS 피드 URL

        Returns:
            뉴스 목록 (제목, 링크, 요약, 출처, 시간)
        """
        try:
            logger.info(f"RSS 피드 수집 중: {feed_url}")
            feed = feedparser.parse(feed_url)

            articles = []
            for entry in feed.entries[:config.NEWS_COLLECTION["max_articles"]]:
                article = {
                    "title": entry.get("title", "제목 없음"),
                    "link": entry.get("link", ""),
                    "summary": entry.get("summary", "요약 없음"),
                    "source": feed.feed.get("title", "출처 불명"),
                    "published": entry.get("published", datetime.now().isoformat()),
                    "collected_at": datetime.now().isoformat(),
                }
                articles.append(article)

            logger.info(f"수집 완료: {len(articles)}개 기사")
            return articles

        except Exception as e:
            logger.error(f"RSS 피드 수집 실패: {str(e)}")
            return []

    def collect_from_sources(self) -> List[Dict]:
        """
        설정된 모든 뉴스 소스에서 뉴스를 수집합니다.

        Returns:
            수집된 뉴스 목록 (최대 max_articles개)
        """
        all_news = []

        # 구글 뉴스 RSS (자동차 스프링 관련)
        google_rss_url = (
            "https://news.google.com/rss/search?q="
            "자동차+스프링+부품&hl=ko&gl=KR&ceid=KR:ko"
        )
        all_news.extend(self.collect_from_rss(google_rss_url))

        # 국내 자동차 뉴스 RSS
        automotive_rss_urls = [
            "https://rss.naver.com/industry/automotive.xml",
            "https://www.newswire.co.kr/newswire/rss/category_automotive.xml",
        ]

        for url in automotive_rss_urls:
            if len(all_news) >= config.NEWS_COLLECTION["max_articles"]:
                break
            all_news.extend(self.collect_from_rss(url))

        # 중복 제거 (URL 기준)
        unique_news = []
        seen_urls = set()
        for article in all_news:
            if article["link"] not in seen_urls:
                seen_urls.add(article["link"])
                unique_news.append(article)

        # 최대 개수만큼 자르기
        unique_news = unique_news[: config.NEWS_COLLECTION["max_articles"]]

        logger.info(f"총 {len(unique_news)}개 뉴스 수집 완료")
        self.collected_news = unique_news
        return unique_news

    def get_collected_news(self) -> List[Dict]:
        """수집된 뉴스를 반환합니다."""
        return self.collected_news


def collect_news() -> List[Dict]:
    """
    뉴스를 수집합니다.

    Returns:
        수집된 뉴스 목록
    """
    collector = NewsCollector()
    return collector.collect_from_sources()


if __name__ == "__main__":
    # 테스트
    logging.basicConfig(level=logging.INFO)
    news = collect_news()
    for i, article in enumerate(news, 1):
        print(f"\n[{i}] {article['title']}")
        print(f"출처: {article['source']}")
        print(f"링크: {article['link']}")
        print(f"요약: {article['summary'][:100]}...")
