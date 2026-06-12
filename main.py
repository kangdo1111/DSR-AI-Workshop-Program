"""
자동차 스프링 업계 뉴스 자동화 시스템 - 메인 실행 파일 (하네스 아키텍처)

매일 아침 8시에 자동으로 뉴스를 수집, 분석, 리포트 생성합니다.

🎯 하네스 아키텍처:
  Coordinator (News Coordinator Agent) 조정 아래
  ├── Collector Agent  (RSS 수집)
  ├── Analyzer Agent   (AI 분석)
  ├── Validator Agent  (품질 검증)
  └── Reporter Agent   (리포트 생성)
"""
import logging
import sys
import os
import json
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

# 환경변수 로드
load_dotenv(Path(__file__).parent / ".env")

# 모듈 임포트
import config
from modules.news_collector import collect_news
from modules.ai_analyzer import analyze_news
from modules.report_generator import generate_report
from modules.scheduler import create_scheduler

# 하네스 스킬 임포트
from skills.collect_news import NewsCollector
from skills.analyze_ai import NewsAnalyzer
from skills.validate_news import NewsValidator
from skills.generate_report import ReportGenerator
from skills.issue_writer import IssueWriter
from skills.issue_runner import IssueRunner

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


def harness_coordinator():
    """
    🎯 하네스 조정자 - Managed Agents 기반 오케스트레이션

    순서:
    1. Collector Agent - RSS 피드 수집 및 필터링
    2. Analyzer Agent - Claude AI 분석
    3. Validator Agent - 품질 검증
    4. Reporter Agent - HTML 리포트 생성
    5. GitHub 이슈 생성 (필요시)
    """
    logger.info("\n" + "=" * 60)
    logger.info("🎯 하네스 조정자 시작 (Managed Agents)")
    logger.info("=" * 60)

    try:
        workspace_dir = Path("/workspace/data")
        workspace_dir.mkdir(parents=True, exist_ok=True)

        # ===== 1단계: Collector Agent =====
        logger.info("\n[1/5] Collector Agent 실행 중...")
        logger.info("📰 RSS 피드 수집 및 필터링...")
        collector = NewsCollector()
        collect_result = collector.collect(max_articles=10)
        logger.info(f"✅ 수집 완료: {collect_result['total_count']}개 뉴스")

        if collect_result["total_count"] == 0:
            logger.warning("⚠️ 수집된 뉴스가 없습니다. 중단합니다.")
            return

        # ===== 2단계: Analyzer Agent =====
        logger.info("\n[2/5] Analyzer Agent 실행 중...")
        logger.info("🤖 Claude AI로 뉴스 분석...")
        analyzer = NewsAnalyzer()
        analyze_result = analyzer.analyze_all()
        logger.info(f"✅ 분석 완료: {analyze_result['total_count']}개 뉴스")

        # ===== 3단계: Validator Agent =====
        logger.info("\n[3/5] Validator Agent 실행 중...")
        logger.info("✅ 품질 검증...")
        validator = NewsValidator()
        validate_result = validator.validate_all()
        logger.info(f"✅ 검증 완료: {validate_result['total_count']}개 승인")
        logger.info(f"   승인율: {validate_result['validation_summary']['approval_rate']:.1%}")

        # ===== 4단계: Reporter Agent =====
        logger.info("\n[4/5] Reporter Agent 실행 중...")
        logger.info("📊 HTML 리포트 생성...")
        reporter = ReportGenerator()
        report_result = reporter.generate()
        if report_result.get("status") == "success":
            logger.info(f"✅ 리포트 생성 완료")
            logger.info(f"   경로: {report_result.get('report_path')}")
        else:
            logger.warning(f"⚠️ 리포트 생성 실패: {report_result.get('message')}")

        # ===== 5단계: GitHub 이슈 생성 =====
        logger.info("\n[5/5] GitHub 이슈 생성...")
        issue_writer = IssueWriter()
        issue_result = issue_writer.run()
        if issue_result.get("status") == "success":
            logger.info(f"✅ GitHub 이슈 생성: {issue_result.get('issues_count')}개")
        else:
            logger.info(f"ℹ️ {issue_result.get('message')}")

        # ===== 결과 정리 =====
        logger.info("\n" + "=" * 60)
        logger.info("✅ 하네스 조정자 완료")
        logger.info("=" * 60)
        logger.info(f"📊 최종 결과:")
        logger.info(f"   수집: {collect_result['total_count']}개")
        logger.info(f"   분석: {analyze_result['total_count']}개")
        logger.info(f"   검증: {validate_result['total_count']}개")
        logger.info(f"   이슈: {issue_result.get('issues_count', 0)}개")

    except Exception as e:
        logger.error(f"❌ 하네스 조정자 오류: {str(e)}", exc_info=True)


def daily_task():
    """
    매일 8시에 실행되는 메인 작업:

    - 모드 1: 하네스 아키텍처 (기본) - Managed Agents 기반
    - 모드 2: 레거시 파이프라인 (기존) - 직접 함수 호출
    """
    use_harness = os.getenv("USE_HARNESS", "true").lower() == "true"

    if use_harness:
        # 🎯 하네스 아키텍처 사용
        harness_coordinator()
    else:
        # 📝 레거시 파이프라인 사용
        try:
            logger.info("=" * 60)
            logger.info("📰 자동차 스프링 업계 뉴스 자동화 시스템 시작 (레거시)")
            logger.info("=" * 60)

            # 1단계: 뉴스 수집
            logger.info("[1/3] 뉴스 수집 중...")
            news_list = collect_news()

            if not news_list or len(news_list) == 0:
                logger.warning("⚠️ 실제 뉴스 수집 실패 - RSS 피드 연결 확인 필요")
                logger.info("샘플 데이터로 계속 진행합니다.")

            logger.info(f"✓ {len(news_list) if news_list else 0}개의 뉴스 수집 완료")

            # 2단계: AI 분석
            logger.info("[2/3] Claude AI로 뉴스 분석 중...")
            analysis_result = analyze_news(news_list)

            summaries = analysis_result.get("summaries", [])
            top_issues = analysis_result.get("top_issues", [])
            keywords = analysis_result.get("keywords", [])

            if "error" in analysis_result:
                logger.warning(f"분석 중 오류 발생: {analysis_result['error']}")
            else:
                logger.info(f"✓ 분석 완료: {len(summaries)}개 요약, {len(top_issues)}개 이슈")

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
