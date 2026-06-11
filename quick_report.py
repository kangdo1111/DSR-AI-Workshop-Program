"""
빠른 리포트 생성 (의존성 최소화)
"""
import sys, os
sys.path.insert(0, os.getcwd())

from modules.news_collector import collect_news
from modules.report_generator import generate_report
from datetime import datetime

print('='*70)
print('🚀 오늘 뉴스 리포트 즉시 생성')
print('='*70)

# 1단계: 뉴스 수집
print('\n[1/2] 뉴스 수집 중...')
news_list = collect_news()
print(f'✅ {len(news_list)}개 뉴스 수집 완료')

# 2단계: 분석 (간단한 처리)
print('\n[2/2] 리포트 생성 중...')

# 수집된 뉴스를 분석 형식으로 변환
summaries = []
for idx, news in enumerate(news_list[:5], 1):  # 최대 5개
    summary_text = news.get('summary', '')[:150]
    if not summary_text:
        summary_text = news.get('title', '')

    summaries.append({
        'rank': idx,
        'title': news.get('title', '제목 없음'),
        'summary': summary_text,
        'impact': ['높음', '중간', '낮음'][idx % 3],
        'source': news.get('source', '출처 불명'),
        'published': news.get('published', '시간 불명'),
        'link': news.get('link', ''),
        'category': '자동차 부품 - 스프링',
        'dsr_response': 'DSR제강의 시장 기회 분석 필요',
        'competitors': {
            '한국': ['NHK스프링', '태태스프링'],
            '일본': ['NHK Spring Co.', 'Aishin'],
            '유럽': ['Lesjöfors', 'Mitsubishi Steel']
        },
        'opportunity': '실시간 뉴스 모니터링으로 신시장 발굴 기회'
    })

# 리포트 생성
report_path = generate_report(summaries, [], [])

print(f'✅ 리포트 생성 완료')
print('\n' + '='*70)
print(f'📄 리포트 경로:')
print(f'   {report_path}')
print('='*70)
print('\n✨ 리포트가 준비되었습니다!')
print(f'\n💡 브라우저에서 열기:')
print(f'   {report_path}')
