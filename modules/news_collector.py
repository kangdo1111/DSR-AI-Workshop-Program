"""
뉴스 수집 모듈 - RSS 피드에서 자동차 스프링 관련 뉴스를 수집합니다.
"""
import feedparser
import requests
import logging
from datetime import datetime, timedelta
from typing import List, Dict
from bs4 import BeautifulSoup
import sys
import os
from email.utils import parsedate_to_datetime
from difflib import SequenceMatcher

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
        sources_tried = 0
        sources_success = 0

        # 구글 뉴스 RSS (자동차 스프링 관련)
        google_rss_urls = [
            "https://news.google.com/rss/search?q=자동차+스프링&hl=ko&gl=KR&ceid=KR:ko",
            "https://news.google.com/rss/search?q=자동차+부품+스프링&hl=ko&gl=KR&ceid=KR:ko",
        ]

        for url in google_rss_urls:
            if len(all_news) >= config.NEWS_COLLECTION["max_articles"]:
                break
            sources_tried += 1
            news = self.collect_from_rss(url)
            if news:
                sources_success += 1
                all_news.extend(news)

        # 국내 자동차 뉴스 RSS
        automotive_rss_urls = [
            "https://rss.naver.com/industry/automotive.xml",
            "https://www.newswire.co.kr/newswire/rss/category_automotive.xml",
        ]

        for url in automotive_rss_urls:
            if len(all_news) >= config.NEWS_COLLECTION["max_articles"]:
                break
            sources_tried += 1
            news = self.collect_from_rss(url)
            if news:
                sources_success += 1
                all_news.extend(news)

        # 중복 제거 (URL 기준)
        unique_news = []
        seen_urls = set()
        for article in all_news:
            if article["link"] and article["link"] not in seen_urls:
                seen_urls.add(article["link"])
                unique_news.append(article)
            elif not article["link"]:
                # 링크가 없으면 제목+시간으로 중복 확인
                key = f"{article['title']}_{article['published']}"
                if key not in seen_urls:
                    seen_urls.add(key)
                    unique_news.append(article)

        # 최대 개수만큼 자르기
        unique_news = unique_news[: config.NEWS_COLLECTION["max_articles"]]

        # 중복 제거 (유사도 80% 이상)
        dedup_news = self.remove_duplicates(unique_news, similarity_threshold=0.8)

        # 스프링 관련성 필터
        relevant_news = self.filter_by_relevance(dedup_news)

        # 날짜 필터링 (최근 7일만)
        filtered_news = self.filter_by_date(relevant_news, days=7)

        logger.info(
            f"총 {len(filtered_news)}개 뉴스 수집 완료 "
            f"(시도: {sources_tried}, 성공: {sources_success})"
        )
        self.collected_news = filtered_news
        return filtered_news

    def get_collected_news(self) -> List[Dict]:
        """수집된 뉴스를 반환합니다."""
        return self.collected_news

    def _similarity_score(self, str1: str, str2: str) -> float:
        """
        두 문자열의 유사도를 계산합니다 (0~1 사이).

        Args:
            str1: 첫 번째 문자열
            str2: 두 번째 문자열

        Returns:
            유사도 점수 (1.0 = 동일)
        """
        return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()

    def filter_by_relevance(self, news_list: List[Dict]) -> List[Dict]:
        """
        스프링/서스펜션 관련 뉴스만 필터링합니다.

        Args:
            news_list: 뉴스 목록

        Returns:
            관련성 있는 뉴스만 필터링된 목록
        """
        # 스프링 관련 키워드
        spring_keywords = [
            "스프링", "spring", "suspension",
            "서스펜션", "현가장치", "완충장치"
        ]

        # 제외 키워드 (스프링 무관)
        exclude_keywords = [
            "IT기술", "소프트웨어", "AI", "인공지능",
            "비트코인", "암호화폐", "주식", "펀드"
        ]

        filtered_news = []

        for article in news_list:
            title = article.get("title", "").lower()
            summary = article.get("summary", "").lower()
            combined_text = f"{title} {summary}"

            # 제외 키워드 확인
            is_excluded = any(
                keyword.lower() in combined_text for keyword in exclude_keywords
            )

            if is_excluded:
                logger.debug(f"제외됨 (관련성 없음): {title[:50]}")
                continue

            # 스프링 키워드 확인
            has_spring_keyword = any(
                keyword.lower() in combined_text for keyword in spring_keywords
            )

            if has_spring_keyword or "자동차" in combined_text and "부품" in combined_text:
                filtered_news.append(article)
            else:
                logger.debug(f"제외됨 (스프링 무관): {title[:50]}")

        logger.info(f"스프링 관련성 필터: {len(news_list)}개 → {len(filtered_news)}개")
        return filtered_news

    def remove_duplicates(
        self, news_list: List[Dict], similarity_threshold: float = 0.8
    ) -> List[Dict]:
        """
        유사한 기사들을 필터링합니다.

        Args:
            news_list: 뉴스 목록
            similarity_threshold: 중복 판정 임계값 (기본값: 0.8)

        Returns:
            중복 제거된 뉴스 목록
        """
        if not news_list:
            return []

        unique_articles = []
        removed_count = 0

        for article in news_list:
            is_duplicate = False

            for existing in unique_articles:
                # 제목 유사도 비교
                title_similarity = self._similarity_score(
                    article.get("title", ""), existing.get("title", "")
                )

                # 요약 유사도 비교
                summary_similarity = self._similarity_score(
                    article.get("summary", "")[:100],
                    existing.get("summary", "")[:100],
                )

                # 둘 다 높으면 중복
                avg_similarity = (title_similarity + summary_similarity) / 2
                if avg_similarity >= similarity_threshold:
                    logger.debug(
                        f"중복 제거: '{article['title'][:50]}' "
                        f"(유사도: {avg_similarity:.2%})"
                    )
                    is_duplicate = True
                    removed_count += 1
                    break

            if not is_duplicate:
                unique_articles.append(article)

        logger.info(f"중복 제거: {len(news_list)}개 → {len(unique_articles)}개 "
                    f"({removed_count}개 제거)")
        return unique_articles

    def filter_by_date(self, news_list: List[Dict], days: int = 7) -> List[Dict]:
        """
        최근 N일 이내의 뉴스만 필터링합니다.

        Args:
            news_list: 뉴스 목록
            days: 포함할 일수 (기본값: 7일)

        Returns:
            필터링된 뉴스 목록
        """
        from datetime import timezone

        # UTC 기준 현재 시간 (aware datetime)
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
        filtered_news = []

        for article in news_list:
            try:
                # RFC 2822 형식의 날짜를 파싱
                if article.get("published"):
                    pub_date = parsedate_to_datetime(article["published"])

                    # naive datetime을 aware datetime으로 변환
                    if pub_date.tzinfo is None:
                        pub_date = pub_date.replace(tzinfo=timezone.utc)

                    if pub_date > cutoff_date:
                        filtered_news.append(article)
                    else:
                        logger.debug(
                            f"날짜 필터 제외: {article['title']} "
                            f"({article['published']})"
                        )
                else:
                    filtered_news.append(article)
            except Exception as e:
                logger.warning(f"날짜 파싱 오류: {str(e)}, 뉴스 포함")
                filtered_news.append(article)

        logger.info(
            f"날짜 필터링: {len(news_list)}개 → {len(filtered_news)}개 "
            f"(최근 {days}일)"
        )
        return filtered_news


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
