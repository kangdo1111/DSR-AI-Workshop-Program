"""
GitHub 이슈 자동 등록 스크립트
ISSUES.md의 8개 이슈를 GitHub에 등록합니다.
"""
import subprocess
import json

ISSUES = [
    {
        "title": "✅ 실제 RSS 피드에서 뉴스 자동 수집 구현",
        "body": """## 문제점
- 현재 ai_analyzer.py에 하드코딩된 테스트 데이터로만 리포트 생성
- 모든 뉴스 링크가 `https://example.com/news/1~10` 더미 URL
- news_collector.py의 실제 RSS 피드 수집 로직이 main.py에서 호출되지 않음

## 해결 방법
✅ news_collector.py 개선 (Google News RSS 2개 URL 추가)
✅ main.py daily_task() 수정 (collect_news() 호출 추가)
✅ 로깅 개선 (시도한 소스/성공한 소스 추적)

## 상태
**완료됨** ✅ | 커밋: `039dd39`

## 검증
- news_collector.py 메서드 존재 확인: ✅
- main.py daily_task()에 collect_news() 호출 추가: ✅
- Google News RSS URL 2개로 확장: ✅""",
        "labels": ["bug", "completed", "news-collection"],
        "state": "open"
    },
    {
        "title": "✅ 지난주·이번주 뉴스만 포함하는 날짜 필터 추가",
        "body": """## 문제점
- 리포트에 2026-06-07(일주일 전) 같은 오래된 기사 포함
- 보고서 날짜: 2026-06-11 (목요일)
- 포함된 기사 날짜 범위: 2026-06-07 ~ 2026-06-11 (불규칙)

## 해결 방법
✅ `filter_by_date()` 메서드 추가 (최근 7일만 필터)
✅ `parsedate_to_datetime` 활용 (RFC 2822 형식 파싱)
✅ `collect_from_sources()` 에 자동 적용

## 상태
**완료됨** ✅ | 커밋: `039dd39`

## 검증
- parsedate_to_datetime 임포트: ✅
- 7일 기준 cutoff_date 계산: ✅
- 예외 처리 (파싱 오류): ✅""",
        "labels": ["enhancement", "completed", "filtering"],
        "state": "open"
    },
    {
        "title": "✅ 동일 사건의 중복 기사 자동 필터링",
        "body": """## 문제점
- 같은 테마의 기사들이 중복으로 포함됨
- 이슈 #1과 뉴스 #1이 동일 주제 (전동화)
- 중복 기사가 리포트를 복잡하게 만들고 신뢰도 저하

## 해결 방법
✅ `_similarity_score()` 메서드 (SequenceMatcher 활용)
✅ `remove_duplicates()` 메서드 (유사도 80% 기준)
✅ 제목+요약 조합 비교로 정확도 향상

## 상태
**완료됨** ✅ | 커밋: `039dd39`

## 검증
- SequenceMatcher 임포트: ✅
- 유사도 계산 알고리즘: ✅
- 평균 유사도 80% 기준: ✅""",
        "labels": ["enhancement", "completed", "deduplication"],
        "state": "open"
    },
    {
        "title": "✅ 자동차 스프링과 무관한 뉴스 제외 필터",
        "body": """## 문제점
- 스프링 산업과 무관한 뉴스들이 포함됨
- 뉴스 #5: "미국, 자동차 부품 재정 지원 확대" (스프링 무관)
- 이슈 #5: "스마트 제조 기술 도입" (IT 기술, 스프링 무관)

## 해결 방법
✅ `filter_by_relevance()` 메서드 추가
✅ 스프링 키워드 필터 (코일, suspension 등)
✅ 제외 키워드 설정 (IT기술, 암호화폐 등)

## 상태
**완료됨** ✅ | 커밋: `039dd39`

## 검증
- spring_keywords 정의: ✅
- exclude_keywords 정의: ✅
- 자동차+부품 조합 인정: ✅""",
        "labels": ["enhancement", "completed", "relevance-filter"],
        "state": "open"
    },
    {
        "title": "🔧 수치 정보에 출처 표기 및 검증 메커니즘 추가",
        "body": """## 문제점
- 뉴스 #2: "특허 **10건** 신청" → 출처 없음
- 뉴스 #4: "스프링 공급 **부족**" → 정량적 수치 없음
- 출처 미표기로 신뢰성 저하

## 계획
1. ai_analyzer.py에서 Claude 응답에 `[출처: OOO]` 형식 추가
2. 수치 없는 표현에 `(미상)` 표기
3. 출처 없는 수치에 ⚠️ 경고 마크 추가
4. report_generator.py에서 시각적 표시

## 우선순위
🔴 높음 (신뢰성 직결)

## 예상 작업량
- 개발: 2시간
- 테스트: 1시간
- 문서화: 1시간""",
        "labels": ["enhancement", "in-progress", "data-quality"],
        "state": "open"
    },
    {
        "title": "🔧 모든 뉴스 링크 유효성 검증",
        "body": """## 문제점
- 테스트 리포트의 모든 링크: `https://example.com/news/1~10` (더미 URL)
- 사용자가 원문 확인 불가능
- 신뢰성 저하

## 계획
1. news_collector.py에서 URL 검증 메서드 추가
2. 404/연결 실패 URL 자동 제외
3. 링크 없는 기사 제외 옵션 추가
4. 유효한 링크만 리포트에 포함

## 우선순위
🟠 중간 (기능성)

## 예상 작업량
- 개발: 2시간
- 테스트: 1시간""",
        "labels": ["enhancement", "in-progress", "link-validation"],
        "state": "open"
    },
    {
        "title": "🔧 리포트 범위를 명확하게 표시",
        "body": """## 문제점
- 현재 제목: "자동차 스프링 업계 뉴스 리포트 - 2026년 6월 11일"
- 불명확: 오늘 뉴스만? 이번주? 지난주?
- 포함된 기사 날짜: 2026-06-07 ~ 2026-06-11 (5일간)

## 계획
1. report_template.html 헤더 수정
2. 명확한 범위 표시: "금주 종합 (2026.06.07~06.13)"
3. 주간/월간 선택 옵션 추가
4. 리포트 하단에 범위 명시

## 우선순위
🟡 낮음 (UI)

## 예상 작업량
- 개발: 1시간""",
        "labels": ["enhancement", "in-progress", "ui"],
        "state": "open"
    },
    {
        "title": "🔧 주요 이슈의 영향도 평가 기준 명확화",
        "body": """## 문제점
- 이슈 우선순위가 근거 없음
- 이슈 #1,2: "높음" (뉴스 중복)
- 이슈 #5: "낮음"인데 포함됨 (스프링 무관)

## 계획
1. ai_analyzer.py에서 뉴스 빈도 기반 이슈 추출
2. 같은 테마 기사 3개 이상만 이슈로 인정
3. 영향도 평가 기준 명문화:
   - **높음**: 규제 변화, 기술 혁신, 공급망 영향
   - **중간**: 산업 동향, 투자 뉴스
   - **낮음**: 개별 기업, 제품 출시
4. 스프링 관련성 0점 이슈 자동 제외

## 우선순위
🟠 중간 (분석 정확도)

## 예상 작업량
- 개발: 2시간
- 테스트: 0.5시간""",
        "labels": ["enhancement", "in-progress", "analytics"],
        "state": "open"
    }
]

def create_issue_with_gh(issue):
    """GitHub CLI로 이슈 생성"""
    try:
        cmd = [
            "gh", "issue", "create",
            "--title", issue["title"],
            "--body", issue["body"],
            "--label", ",".join(issue["labels"])
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            return True, result.stdout.strip()
        else:
            return False, result.stderr.strip()
    except Exception as e:
        return False, str(e)

def main():
    print("="*70)
    print("📋 GitHub 이슈 등록 시작")
    print("="*70)

    success_count = 0
    failed_count = 0

    for idx, issue in enumerate(ISSUES, 1):
        print(f"\n[{idx}/8] {issue['title'][:50]}...")

        success, message = create_issue_with_gh(issue)

        if success:
            print(f"  ✅ 등록 완료")
            success_count += 1
        else:
            print(f"  ❌ 실패: {message[:100]}")
            failed_count += 1

    print("\n" + "="*70)
    print(f"결과: ✅ {success_count}개 등록 / ❌ {failed_count}개 실패")
    print("="*70)

if __name__ == "__main__":
    main()
