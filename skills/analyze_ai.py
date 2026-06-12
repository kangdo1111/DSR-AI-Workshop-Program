"""
analyze-ai 스킬: Claude AI를 사용한 뉴스 분석

Analyzer Agent가 사용하는 메인 스킬입니다.
수집된 뉴스를 Claude AI로 전문가 수준으로 분석합니다.
"""

import json
import os
from pathlib import Path
from datetime import datetime
from anthropic import Anthropic

client = Anthropic()


class NewsAnalyzer:
    """Claude AI 기반 뉴스 분석"""

    ANALYSIS_PROMPT = """당신은 자동차 스프링 업계의 20년 전문가입니다.

다음 뉴스를 분석하고 JSON 형식으로 답변해주세요:

**뉴스 제목**: {title}
**뉴스 내용**: {content}
**출처**: {source}

다음 항목을 분석하세요:

1. **기술적 영향도**: High/Medium/Low (새로운 기술, 재료, 공정 등에 미치는 영향)
2. **시장 영향도**: High/Medium/Low (수요, 경쟁, 가격 등에 미치는 영향)
3. **이슈 카테고리**: 신기술/정책/경제/경쟁/기타 중 선택
4. **핵심 요약**: 3-5 문장으로 자동차 스프링 업계 관점에서 요약
5. **통계/수치**: 뉴스에 언급된 구체적인 수치나 통계 (없으면 "없음")
6. **출처 명시**: "[출처: OOO]" 형식
7. **주요 이슈**: 이 뉴스가 제시하는 핵심 문제점이나 기회

JSON 응답 형식:
```json
{
    "technical_impact": "High|Medium|Low",
    "market_impact": "High|Medium|Low",
    "category": "신기술|정책|경제|경쟁|기타",
    "summary": "...",
    "statistics": "...",
    "source_citation": "[출처: ...]",
    "key_issues": ["...", "..."],
    "analysis_date": "YYYY-MM-DD"
}
```"""

    def __init__(self):
        self.workspace_dir = Path("/workspace/data")
        self.workspace_dir.mkdir(parents=True, exist_ok=True)
        self.api_key = os.getenv("ANTHROPIC_API_KEY")

    def analyze_article(self, article: dict) -> dict:
        """단일 뉴스 분석"""
        prompt = self.ANALYSIS_PROMPT.format(
            title=article.get("title", ""),
            content=article.get("content", "")[:1000],  # 처음 1000자만
            source=article.get("source", "")
        )

        try:
            response = client.messages.create(
                model="claude-opus-4-8",
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )

            analysis_text = response.content[0].text

            # JSON 추출
            try:
                json_start = analysis_text.find("{")
                json_end = analysis_text.rfind("}") + 1
                if json_start >= 0 and json_end > json_start:
                    analysis = json.loads(analysis_text[json_start:json_end])
                else:
                    analysis = self._parse_fallback(analysis_text)
            except json.JSONDecodeError:
                analysis = self._parse_fallback(analysis_text)

            return {
                **article,
                "analysis": analysis,
                "analyzed_at": datetime.now().isoformat()
            }

        except Exception as e:
            print(f"Error analyzing article: {e}")
            return {
                **article,
                "analysis": {
                    "technical_impact": "Unknown",
                    "market_impact": "Unknown",
                    "category": "기타",
                    "summary": article.get("content", ""),
                    "statistics": "없음",
                    "source_citation": f"[출처: {article.get('source', '')}]",
                    "key_issues": [],
                    "analysis_date": datetime.now().strftime("%Y-%m-%d")
                },
                "analyzed_at": datetime.now().isoformat(),
                "error": str(e)
            }

    def _parse_fallback(self, text: str) -> dict:
        """JSON 파싱 실패시 폴백"""
        return {
            "technical_impact": "Unknown",
            "market_impact": "Unknown",
            "category": "기타",
            "summary": text[:200],
            "statistics": "없음",
            "source_citation": "",
            "key_issues": [],
            "analysis_date": datetime.now().strftime("%Y-%m-%d")
        }

    def analyze_all(self) -> dict:
        """수집된 모든 뉴스 분석"""
        # 수집된 뉴스 읽기
        input_file = self.workspace_dir / "collected_news.json"

        if not input_file.exists():
            print("[Analyzer] 수집된 뉴스 파일을 찾을 수 없습니다.")
            return {"analyzed": [], "total": 0}

        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        articles = data.get("articles", [])
        print(f"[Analyzer] {len(articles)}개 뉴스 분석 중...")

        analyzed_articles = []
        for i, article in enumerate(articles, 1):
            print(f"[Analyzer] {i}/{len(articles)} 분석 중: {article['title'][:50]}")
            analyzed = self.analyze_article(article)
            analyzed_articles.append(analyzed)

        result = {
            "timestamp": datetime.now().isoformat(),
            "total_count": len(analyzed_articles),
            "articles": analyzed_articles
        }

        # 결과 저장
        output_file = self.workspace_dir / "analyzed_news.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"[Analyzer] 분석 완료. 결과 저장: {output_file}")
        return result


def run_skill() -> dict:
    """스킬 실행"""
    analyzer = NewsAnalyzer()
    return analyzer.analyze_all()


if __name__ == "__main__":
    result = run_skill()
    print("\n=== 분석 결과 ===")
    print(f"분석된 뉴스: {result['total_count']}개")
