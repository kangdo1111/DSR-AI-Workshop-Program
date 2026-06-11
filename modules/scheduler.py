"""
스케줄링 모듈 - APScheduler를 사용하여 매일 8시에 자동으로 작업을 실행합니다.
"""
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from typing import Callable
import sys
import os

# config.py 경로 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

logger = logging.getLogger(__name__)


class NewsScheduler:
    """뉴스 수집 및 보고서 생성을 스케줄링하는 클래스"""

    def __init__(self):
        self.scheduler = BackgroundScheduler(
            timezone=config.SCHEDULER["timezone"]
        )

    def start_scheduler(self, task_func: Callable) -> None:
        """
        스케줄러를 시작합니다.

        Args:
            task_func: 매일 실행할 함수
        """
        try:
            # 매일 8시에 실행되도록 설정
            self.scheduler.add_job(
                task_func,
                "cron",
                hour=config.SCHEDULER["hour"],
                minute=config.SCHEDULER["minute"],
                id="daily_news_task",
                name="Daily News Collection and Report Generation",
                misfire_grace_time=600,
                coalesce=True,
            )

            self.scheduler.start()
            logger.info(
                f"스케줄러 시작됨. 매일 {config.SCHEDULER['hour']}:{config.SCHEDULER['minute']:02d}에 실행됩니다."
            )

        except Exception as e:
            logger.error(f"스케줄러 시작 실패: {str(e)}")
            raise

    def stop_scheduler(self) -> None:
        """스케줄러를 중지합니다."""
        try:
            self.scheduler.shutdown(wait=True)
            logger.info("스케줄러가 중지되었습니다.")
        except Exception as e:
            logger.error(f"스케줄러 중지 실패: {str(e)}")

    def is_running(self) -> bool:
        """
        스케줄러 실행 여부를 확인합니다.

        Returns:
            실행 중이면 True, 아니면 False
        """
        return self.scheduler.running


def create_scheduler() -> NewsScheduler:
    """
    스케줄러를 생성합니다.

    Returns:
        NewsScheduler 객체
    """
    return NewsScheduler()


if __name__ == "__main__":
    # 테스트
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    def sample_task():
        logger.info("샘플 작업 실행됨")

    scheduler = create_scheduler()
    scheduler.start_scheduler(sample_task)

    try:
        logger.info("스케줄러가 실행 중입니다. Ctrl+C로 종료하세요.")
        while True:
            pass
    except KeyboardInterrupt:
        scheduler.stop_scheduler()
        logger.info("프로그램이 종료되었습니다.")
