"""
오늘 뉴스 리포트 즉시 생성
"""
import sys, os
sys.path.insert(0, os.getcwd())

from modules.news_collector import collect_news
from modules.ai_analyzer import NewsAnalyzer
from modules.report_generator import generate_report
from datetime import datetime

print('='*70)
print('🚀 오늘 뉴스 리포트 즉시 생성')
print('='*70)

# 1단계: 뉴스 수집
print('\n[1/3] 뉴스 수집 중...')
news_list = collect_news()
print(f'✅ {len(news_list)}개 뉴스 수집 완료')

# 2단계: AI 분석
print('\n[2/3] AI 분석 중...')
analyzer = NewsAnalyzer()
analysis = analyzer.analyze_news(news_list)
summaries = analysis.get('summaries', [])
print(f'✅ {len(summaries)}개 뉴스 분석 완료')

# 3단계: 리포트 생성
print('\n[3/3] HTML 리포트 생성 중...')
report_path = generate_report(summaries, [], [])
print(f'✅ 리포트 생성 완료')

print('\n' + '='*70)
print(f'📄 리포트 경로: {report_path}')
print('='*70)

# 브라우저에서 열기 명령 출력
print('\n💡 브라우저에서 열기:')
print(f'   {report_path}')

print('\n✅ 리포트가 준비되었습니다!')
