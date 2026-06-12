"""
뉴스 리포트 생성 - 원래 방식 (간단 버전)
레거시 파이프라인만 사용합니다.
"""

import logging
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# 환경 설정
load_dotenv(Path(__file__).parent / ".env")

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)

# 모듈 임포트
import config
from modules.news_collector import collect_news
from modules.ai_analyzer import analyze_news
from modules.report_generator import generate_report


def main():
    """뉴스 리포트 생성"""
    try:
        logger.info("=" * 70)
        logger.info("📰 자동차 스프링 업계 뉴스 자동화 시스템")
        logger.info("=" * 70)

        # 1단계: 뉴스 수집
        logger.info("\n[1/3] 📰 뉴스 수집 중...")
        news_list = collect_news()

        if not news_list or len(news_list) == 0:
            logger.warning("⚠️ 실제 뉴스 수집 실패")
            logger.error("❌ 작업을 중단합니다.")
            return

        logger.info(f"✅ {len(news_list)}개의 뉴스 수집 완료")

        # 2단계: AI 분석
        logger.info("\n[2/3] 🤖 Claude AI로 뉴스 분석 중...")
        analysis_result = analyze_news(news_list)

        summaries = analysis_result.get("summaries", [])
        top_issues = analysis_result.get("top_issues", [])
        keywords = analysis_result.get("keywords", [])

        if "error" in analysis_result:
            logger.warning(f"⚠️ 분석 중 오류: {analysis_result['error']}")
        else:
            logger.info(
                f"✅ 분석 완료: {len(summaries)}개 요약, {len(top_issues)}개 이슈"
            )

        # 3단계: HTML 리포트 생성
        logger.info("\n[3/3] 📊 HTML 리포트 생성 중...")
        report_path = generate_report(summaries, top_issues, keywords)
        logger.info(f"✅ 리포트 생성 완료!")

        logger.info("\n" + "=" * 70)
        logger.info("📍 리포트 경로:")
        logger.info(f"   {report_path}")
        logger.info("\n🌐 브라우저에서 열기:")
        logger.info(f"   file:///{report_path}")
        logger.info("=" * 70 + "\n")

    except Exception as e:
        logger.error(f"❌ 오류 발생: {str(e)}", exc_info=True)
        print("\n" + "=" * 70)
        print("프로그램이 오류로 중단되었습니다.")
        print("=" * 70)
        input("\n아무 키나 누르세요...")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n예상치 못한 오류: {str(e)}")
        import traceback
        traceback.print_exc()
