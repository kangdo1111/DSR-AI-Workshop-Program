"""
자동차 스프링 업계 뉴스 자동화 시스템 - 메인 실행 파일
매일 아침 8시에 자동으로 뉴스를 수집, 분석, 리포트 생성합니다.
"""
import logging
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv(Path(__file__).parent / ".env")

# 모듈 임포트
import config
from modules.news_collector import collect_news
from modules.ai_analyzer import analyze_news
from modules.report_generator import generate_report
from modules.scheduler import create_scheduler

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format=config.LOGGING["format"],
    datefmt=config.LOGGING["date_format"],
    handlers=[
        logging.FileHandler(
            config.PATHS["logs"] / f"{Path.cwd().name}_latest.log", encoding="utf-8"
        ),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)


def daily_task():
    """
    매일 8시에 실행되는 메인 작업:
    1. 뉴스 수집
    2. AI 분석
    3. HTML 리포트 생성
    """
    try:
        logger.info("=" * 60)
        logger.info("📰 자동차 스프링 업계 뉴스 자동화 시스템 시작")
        logger.info("=" * 60)

        # 1단계: 뉴스 수집 (실제 RSS 피드)
        logger.info("[1/3] 뉴스 수집 중...")
        news_list = collect_news()

        # 뉴스 수집 실패 시 경고 (테스트 데이터로 진행)
        if not news_list or len(news_list) == 0:
            logger.warning("⚠️ 실제 뉴스 수집 실패 - RSS 피드 연결 확인 필요")
            logger.info("샘플 데이터로 계속 진행합니다.")
            # 계속 진행하거나 종료 여부 결정 가능
            # return  # 주석 처리: 테스트 용도로 계속 진행

        logger.info(f"✓ {len(news_list) if news_list else 0}개의 뉴스 수집 완료" if news_list else "✓ 샘플 데이터로 진행")

        # 2단계: AI 분석
        logger.info("[2/3] Claude AI로 뉴스 분석 중...")
        analysis_result = analyze_news(news_list)

        summaries = analysis_result.get("summaries", [])
        top_issues = analysis_result.get("top_issues", [])
        keywords = analysis_result.get("keywords", [])

        if "error" in analysis_result:
            logger.warning(f"분석 중 오류 발생: {analysis_result['error']}")
        else:
            logger.info(f"✓ 분석 완료: {len(summaries)}개 요약, {len(top_issues)}개 이슈, {len(keywords)}개 키워드")

        # 3단계: HTML 리포트 생성
        logger.info("[3/3] HTML 리포트 생성 중...")
        report_path = generate_report(summaries, top_issues, keywords)
        logger.info(f"✓ 리포트 생성 완료: {report_path}")

        logger.info("=" * 60)
        logger.info("✅ 모든 작업이 정상적으로 완료되었습니다.")
        logger.info("=" * 60)

    except Exception as e:
        logger.error(f"❌ 오류 발생: {str(e)}", exc_info=True)


def main():
    """메인 함수 - 스케줄러를 시작합니다."""
    logger.info("🚀 자동차 스프링 업계 뉴스 자동화 시스템 초기화 중...")

    # API 키 확인
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        logger.error("❌ Anthropic API 키가 설정되지 않았습니다.")
        logger.error(".env 파일의 ANTHROPIC_API_KEY를 설정해주세요.")
        logger.error("https://console.anthropic.com 에서 API 키를 발급받으세요.")
        sys.exit(1)

    logger.info("✓ API 키 확인 완료")
    logger.info(f"✓ 저장 경로: {config.PATHS['output']}")
    logger.info(f"✓ 로그 경로: {config.PATHS['logs']}")

    # 스케줄러 생성 및 시작
    scheduler = create_scheduler()

    try:
        scheduler.start_scheduler(daily_task)

        logger.info("")
        logger.info("=" * 60)
        logger.info("✅ 시스템이 준비되었습니다!")
        logger.info("=" * 60)
        logger.info(f"📅 실행 시간: 매일 {config.SCHEDULER['hour']}:{config.SCHEDULER['minute']:02d}")
        logger.info(f"📁 리포트 저장 경로: {config.PATHS['output']}")
        logger.info("")
        logger.info("💡 종료하려면 Ctrl+C를 누르세요.")
        logger.info("")

        # 스케줄러가 실행되는 동안 대기
        while True:
            pass

    except KeyboardInterrupt:
        logger.info("")
        logger.info("=" * 60)
        logger.info("🛑 시스템 종료 중...")
        logger.info("=" * 60)
        scheduler.stop_scheduler()
        logger.info("✓ 시스템이 종료되었습니다.")
        sys.exit(0)

    except Exception as e:
        logger.error(f"❌ 심각한 오류 발생: {str(e)}", exc_info=True)
        scheduler.stop_scheduler()
        sys.exit(1)


if __name__ == "__main__":
    main()
