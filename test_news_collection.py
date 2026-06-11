"""
실제 RSS 피드 수집 테스트
"""
import sys, os
sys.path.insert(0, os.getcwd())

from modules.news_collector import collect_news
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')

print('='*70)
print('📰 실제 RSS 피드에서 뉴스 수집 테스트')
print('='*70)

news = collect_news()

print(f'\n✅ 최종 수집된 뉴스: {len(news)}개')
print('(최대 5개까지만 리포트에 표시됨)')
print('='*70)

if news:
    for idx, article in enumerate(news, 1):
        print(f'\n[{idx}] {article["title"][:60]}')
        print(f'    📍 출처: {article["source"]}')
        print(f'    🔗 링크: {article["link"][:55]}...')
        print(f'    ⏰ 시간: {article["published"]}')
else:
    print('\n⚠️ 수집된 뉴스가 없습니다.')
    print('(RSS 피드 연결 실패 또는 스프링 관련 뉴스 없음)')

print('\n' + '='*70)
