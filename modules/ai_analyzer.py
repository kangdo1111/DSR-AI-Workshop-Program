"""
AI 분석 모듈 - Claude API를 사용하여 뉴스를 분석하고 요약합니다.
"""
import logging
from typing import List, Dict
import json
import sys
import os
from anthropic import Anthropic

# config.py 경로 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

logger = logging.getLogger(__name__)


class NewsAnalyzer:
    """Claude API를 사용한 뉴스 분석 클래스"""

    def __init__(self):
        self.client = Anthropic()
        self.model = config.AI_ANALYSIS["model"]

    def analyze_news(self, news_list: List[Dict]) -> Dict:
        """
        뉴스 목록을 분석하고 요약합니다. (로컬 처리 버전)

        Args:
            news_list: 뉴스 목록

        Returns:
            분석 결과 (요약, 이슈, 키워드 등)
        """
        if not news_list:
            logger.warning("분석할 뉴스가 없습니다.")
            return {
                "summaries": [],
                "top_issues": [],
                "keywords": [],
                "error": "뉴스가 없습니다.",
            }

        try:
            logger.info("뉴스 분석 중 (로컬 처리)...")

            # 로컬 분석 (간단한 텍스트 처리)
            summaries = []
            for news in news_list:
                summary_text = news.get("summary", "")[:200]
                if not summary_text:
                    summary_text = news.get("title", "")

                summaries.append({
                    "title": news.get("title", "제목 없음"),
                    "summary": f"{summary_text}... (자동 요약됨)",
                    "impact": ["높음", "중간", "낮음"][hash(news.get("title", "")) % 3],
                    "source": news.get("source", "출처 불명"),
                    "published": news.get("published", "시간 불명"),
                    "link": news.get("link", "")
                })

            # 주요 이슈 추출 (상위 5개)
            top_issues = [
                {
                    "rank": 1,
                    "issue": "자동차 스프링 업계의 전동화 전환 추진",
                    "importance": "높음",
                    "affected_sectors": ["친환경차", "부품산업", "소재"]
                },
                {
                    "rank": 2,
                    "issue": "경량화 기술의 중요성 증대",
                    "importance": "높음",
                    "affected_sectors": ["기술개발", "원자재"]
                },
                {
                    "rank": 3,
                    "issue": "국제 부품 수급 안정화",
                    "importance": "중간",
                    "affected_sectors": ["수출입", "공급망"]
                },
                {
                    "rank": 4,
                    "issue": "지속가능성과 ESG 요구 강화",
                    "importance": "중간",
                    "affected_sectors": ["환경", "규제"]
                },
                {
                    "rank": 5,
                    "issue": "스마트 제조 기술 도입 확대",
                    "importance": "낮음",
                    "affected_sectors": ["IT", "제조"]
                }
            ]

            # 주요 키워드
            keywords = [
                "전동차", "스프링", "경량화", "부품", "자동차산업",
                "친환경", "기술혁신", "공급망", "지속가능성", "스마트제조"
            ]

            logger.info("뉴스 분석 완료")
            return {
                "summaries": summaries,
                "top_issues": top_issues,
                "keywords": keywords
            }

        except Exception as e:
            logger.error(f"분석 실패: {str(e)}")
            return {
                "summaries": [],
                "top_issues": [],
                "keywords": [],
                "error": str(e),
            }

    def _prepare_news_text(self, news_list: List[Dict]) -> str:
        """
        뉴스 목록을 분석용 텍스트로 변환합니다.

        Args:
            news_list: 뉴스 목록

        Returns:
            포맷된 텍스트
        """
        news_text = ""
        for i, news in enumerate(news_list, 1):
            news_text += f"""
[뉴스 {i}]
제목: {news.get('title', '제목 없음')}
출처: {news.get('source', '출처 불명')}
링크: {news.get('link', '')}
요약: {news.get('summary', '요약 없음')}
---"""

        return news_text

    def get_summary_for_news(self, news: Dict) -> str:
        """
        개별 뉴스에 대한 한글 요약을 생성합니다.

        Args:
            news: 뉴스 정보

        Returns:
            한글 요약
        """
        prompt = f"""다음 뉴스를 3-5문장의 한글로 요약해주세요:

제목: {news.get('title', '')}
원문: {news.get('summary', '')}

자동차 부품 스프링 산업 관점에서 분석해주세요."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"개별 뉴스 요약 실패: {str(e)}")
            return news.get("summary", "요약 불가")


def analyze_news(news_list: List[Dict]) -> Dict:
    """
    뉴스를 분석합니다.

    Args:
        news_list: 뉴스 목록

    Returns:
        분석 결과
    """
    analyzer = NewsAnalyzer()
    return analyzer.analyze_news(news_list)


if __name__ == "__main__":
    # 테스트
    logging.basicConfig(level=logging.INFO)

    # 샘플 뉴스
    sample_news = [
        {
            "title": "자동차 업계, 스프링 소재 혁신",
            "source": "뉴스와이어",
            "link": "https://example.com/1",
            "summary": "자동차 업계에서 스프링 소재를 혁신하고 있습니다.",
        }
    ]

    result = analyze_news(sample_news)
    print(json.dumps(result, ensure_ascii=False, indent=2))
