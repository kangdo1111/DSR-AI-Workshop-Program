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
        뉴스 목록을 분석하고 요약합니다.

        Args:
            news_list: 뉴스 목록

        Returns:
            분석 결과 (요약, 이슈, 키워드 등)
        """
        if not news_list:
            logger.warning("분석할 뉴스가 없습니다.")
            return {
                "summaries": [],
                "issues": [],
                "keywords": [],
                "error": "뉴스가 없습니다.",
            }

        # 뉴스 전문 준비
        news_text = self._prepare_news_text(news_list)

        try:
            logger.info("Claude AI로 뉴스 분석 중...")

            # 전체 분석을 위한 프롬프트
            analysis_prompt = f"""다음은 자동차 부품 스프링 산업 관련 뉴스입니다.
당신은 20년 경력의 자동차 부품 업계 전문가입니다.

뉴스 목록:
{news_text}

다음 작업을 수행해주세요:

1. 각 뉴스를 3-5문장의 한글 요약으로 작성
2. 각 뉴스의 스프링 산업에 미치는 영향도 평가 (높음/중간/낮음)
3. 전체 뉴스에서 가장 중요한 이슈 5개 추출
4. 주요 키워드 5-10개 도출

다음 JSON 형식으로 응답해주세요:
{{
    "summaries": [
        {{
            "title": "원본 제목",
            "summary": "한글 요약",
            "impact": "높음/중간/낮음",
            "link": "원본 링크"
        }}
    ],
    "top_issues": [
        {{
            "rank": 1,
            "issue": "이슈 내용",
            "importance": "높음/중간/낮음",
            "affected_sectors": ["부채"]
        }}
    ],
    "keywords": ["키워드1", "키워드2", ...]
}}"""

            response = self.client.messages.create(
                model=self.model,
                max_tokens=config.AI_ANALYSIS["max_tokens"],
                messages=[{"role": "user", "content": analysis_prompt}],
            )

            response_text = response.content[0].text

            # JSON 추출
            try:
                # JSON 부분 추출
                json_start = response_text.find("{")
                json_end = response_text.rfind("}") + 1
                json_str = response_text[json_start:json_end]
                analysis_result = json.loads(json_str)
                logger.info("뉴스 분석 완료")
                return analysis_result
            except json.JSONDecodeError:
                logger.error("JSON 파싱 실패, 전체 응답 반환")
                return {
                    "summaries": [],
                    "top_issues": [],
                    "keywords": [],
                    "raw_response": response_text,
                }

        except Exception as e:
            logger.error(f"Claude API 호출 실패: {str(e)}")
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
