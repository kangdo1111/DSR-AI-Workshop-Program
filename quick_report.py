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

# 뉴스가 없으면 샘플 데이터 사용
if not news_list:
    print('(최근 뉴스 없음 → 샘플 데이터로 진행)')
    news_list = [
        {
            "title": "현대차, 신형 전기차용 고강도 스프링 기술 공개",
            "summary": "현대자동차가 전동화 추세에 맞춰 자동차 스프링의 고강도화 기술을 발표했습니다.",
            "source": "자동차 업계 뉴스",
            "published": "2026-06-11 10:00:00",
            "link": "https://news.example.com/1"
        },
        {
            "title": "자동차 부품 업체, 경량화 스프링 소재 개발 완료",
            "summary": "자동차 스프링 제조사들이 경량화 소재로 무게를 30% 줄였습니다.",
            "source": "부품 산업 뉴스",
            "published": "2026-06-10 15:30:00",
            "link": "https://news.example.com/2"
        },
        {
            "title": "국제 표준화 기구, 자동차 스프링 새 안전 기준 발표",
            "summary": "ISO에서 친환경 소재 사용 의무화 기준을 새로 제정했습니다.",
            "source": "국제 표준 뉴스",
            "published": "2026-06-09 08:45:00",
            "link": "https://news.example.com/3"
        },
        {
            "title": "토요타, 서스펜션 시스템 혁신으로 탄소 배출 감축",
            "summary": "토요타가 스프링 기술 혁신으로 차량의 탄소 배출을 추가로 감축했습니다.",
            "source": "완성차 뉴스",
            "published": "2026-06-08 12:20:00",
            "link": "https://news.example.com/4"
        },
        {
            "title": "BMW, 고성능 토션 바 기술 특허 출원",
            "summary": "BMW가 경량 고성능 토션 바 기술로 국제 특허를 출원했습니다.",
            "source": "특허 뉴스",
            "published": "2026-06-07 16:15:00",
            "link": "https://news.example.com/5"
        }
    ]

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
