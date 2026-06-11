"""
리포트 생성 모듈 - HTML 템플릿을 사용하여 전문적인 뉴스 리포트를 생성합니다.
"""
import logging
from typing import List, Dict
from pathlib import Path
from datetime import datetime
from jinja2 import Template
import sys
import os

# config.py 경로 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

logger = logging.getLogger(__name__)


class ReportGenerator:
    """HTML 리포트 생성 클래스"""

    def __init__(self):
        self.template_path = config.PATHS["templates"] / "report_template.html"
        self.output_path = config.PATHS["output"]

    def generate_report(
        self, summaries: List[Dict], top_issues: List[Dict], keywords: List[str]
    ) -> str:
        """
        HTML 리포트를 생성합니다.

        Args:
            summaries: 뉴스 요약 목록
            top_issues: 주요 이슈 목록
            keywords: 키워드 목록

        Returns:
            저장된 리포트 파일 경로
        """
        try:
            logger.info("리포트 생성 중...")

            # 템플릿 로드
            with open(self.template_path, "r", encoding="utf-8") as f:
                template_str = f.read()

            template = Template(template_str)

            # 현재 시간 정보
            now = datetime.now()
            report_date = now.strftime("%Y년 %m월 %d일")
            report_date_kr = self._format_korean_date(now)
            generated_at = now.strftime("%Y-%m-%d %H:%M:%S")

            # 템플릿 렌더링
            html_content = template.render(
                summaries=summaries,
                top_issues=top_issues,
                keywords=keywords,
                report_date=report_date,
                report_date_kr=report_date_kr,
                generated_at=generated_at,
            )

            # 파일 저장
            output_file = self._get_output_file_path(now)
            output_file.parent.mkdir(parents=True, exist_ok=True)

            with open(output_file, "w", encoding="utf-8") as f:
                f.write(html_content)

            logger.info(f"리포트 생성 완료: {output_file}")
            return str(output_file)

        except Exception as e:
            logger.error(f"리포트 생성 실패: {str(e)}")
            raise

    def _format_korean_date(self, date: datetime) -> str:
        """
        날짜를 한글 형식으로 변환합니다.

        Args:
            date: datetime 객체

        Returns:
            한글 형식의 날짜 문자열
        """
        days = ["월", "화", "수", "목", "금", "토", "일"]
        day_name = days[date.weekday()]
        return date.strftime(f"%Y년 %m월 %d일 ({day_name}요일)")

    def _get_output_file_path(self, date: datetime) -> Path:
        """
        출력 파일 경로를 생성합니다.

        Args:
            date: datetime 객체

        Returns:
            파일 경로
        """
        date_folder = date.strftime("%Y-%m-%d")
        output_file = self.output_path / date_folder / "report.html"
        return output_file

    def generate_summary_html(self, news_title: str, summary: str) -> str:
        """
        뉴스 요약을 HTML 형식으로 변환합니다.

        Args:
            news_title: 뉴스 제목
            summary: 뉴스 요약

        Returns:
            HTML 문자열
        """
        html = f"""
        <div class="summary-item">
            <h4>{news_title}</h4>
            <p>{summary}</p>
        </div>
        """
        return html


def generate_report(
    summaries: List[Dict], top_issues: List[Dict], keywords: List[str]
) -> str:
    """
    리포트를 생성합니다.

    Args:
        summaries: 뉴스 요약 목록
        top_issues: 주요 이슈 목록
        keywords: 키워드 목록

    Returns:
        저장된 리포트 파일 경로
    """
    generator = ReportGenerator()
    return generator.generate_report(summaries, top_issues, keywords)


if __name__ == "__main__":
    # 테스트
    logging.basicConfig(level=logging.INFO)

    # 샘플 데이터
    sample_summaries = [
        {
            "title": "자동차 업계, 경량화 기술 혁신",
            "summary": "최근 자동차 산업에서 경량화 기술이 주목받고 있습니다. 스프링 소재의 고강도화를 통해 무게를 줄이면서도 안전성을 유지하는 기술이 개발되고 있습니다.",
            "impact": "높음",
            "source": "뉴스와이어",
            "published": "2026-06-11 10:30",
            "link": "https://example.com/news/1",
        }
    ]

    sample_issues = [
        {
            "rank": 1,
            "issue": "전동차 확대에 따른 스프링 수요 변화",
            "importance": "높음",
            "affected_sectors": ["친환경차", "부품산업"],
        }
    ]

    sample_keywords = ["전동차", "스프링", "경량화", "안전성", "친환경"]

    report_path = generate_report(sample_summaries, sample_issues, sample_keywords)
    print(f"리포트 생성됨: {report_path}")
