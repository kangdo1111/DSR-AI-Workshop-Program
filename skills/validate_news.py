"""
validate-news 스킬: 뉴스 품질 및 관련성 검증

Validator Agent가 사용하는 메인 스킬입니다.
분석된 뉴스의 품질과 관련성을 재검증합니다.
"""

import json
from pathlib import Path
from datetime import datetime


class NewsValidator:
    """뉴스 검증"""

    TRUSTED_SOURCES = {
        "한국경제": 0.95,
        "매일경제": 0.95,
        "동아일보": 0.9,
        "조선일보": 0.9,
        "중앙일보": 0.9,
        "한국일보": 0.85,
        "경향신문": 0.85,
        "뉴스와이어": 0.9,
        "이뉴스투데이": 0.85,
        "아이뉴스24": 0.8,
        "google_news": 0.7,
        "naver_news": 0.7
    }

    def __init__(self):
        self.workspace_dir = Path("/workspace/data")
        self.workspace_dir.mkdir(parents=True, exist_ok=True)

    def get_source_credibility(self, source: str) -> float:
        """출처 신뢰도 점수"""
        for trusted_source, credibility in self.TRUSTED_SOURCES.items():
            if trusted_source.lower() in source.lower():
                return credibility
        return 0.5  # 알려지지 않은 출처

    def validate_article(self, article: dict) -> dict:
        """단일 뉴스 검증"""
        validation = {
            "source_credibility": 0.0,
            "relevance_score": 0.0,
            "analysis_quality": 0.0,
            "source_citation_present": False,
            "issues": [],
            "approved": False
        }

        # 1. 출처 신뢰도
        source_credibility = self.get_source_credibility(article.get("source", ""))
        validation["source_credibility"] = source_credibility

        # 2. 관련성 점수 (분석의 기술적 영향도 기반)
        analysis = article.get("analysis", {})
        technical_impact = analysis.get("technical_impact", "Low")
        impact_scores = {"High": 0.9, "Medium": 0.7, "Low": 0.5}
        relevance_score = impact_scores.get(technical_impact, 0.5)
        validation["relevance_score"] = relevance_score

        # 3. 분석 품질 체크
        quality_issues = []
        if not analysis.get("summary"):
            quality_issues.append("요약이 없음")
        if not analysis.get("key_issues"):
            quality_issues.append("주요 이슈가 미흡")

        analysis_quality = 1.0 - (len(quality_issues) * 0.2)
        validation["analysis_quality"] = max(0.5, analysis_quality)

        if quality_issues:
            validation["issues"].extend(quality_issues)

        # 4. 출처 인용 확인
        source_citation = analysis.get("source_citation", "")
        if source_citation and "[출처:" in source_citation:
            validation["source_citation_present"] = True
        else:
            if "statistics" in analysis and analysis["statistics"] != "없음":
                validation["issues"].append("⚠️ 통계 출처 없음")

        # 5. 최종 승인 여부
        # 출처 신뢰도 >= 0.5 AND 관련성 >= 0.7 AND 분석 품질 >= 0.6
        validation["approved"] = (
            source_credibility >= 0.5 and
            relevance_score >= 0.7 and
            validation["analysis_quality"] >= 0.6
        )

        return {
            **article,
            "validation": validation
        }

    def validate_all(self) -> dict:
        """모든 뉴스 검증"""
        # 분석된 뉴스 읽기
        input_file = self.workspace_dir / "analyzed_news.json"

        if not input_file.exists():
            print("[Validator] 분석된 뉴스 파일을 찾을 수 없습니다.")
            return {"validated": [], "total": 0, "approved_count": 0}

        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        articles = data.get("articles", [])
        print(f"[Validator] {len(articles)}개 뉴스 검증 중...")

        validated_articles = []
        approved_count = 0

        for i, article in enumerate(articles, 1):
            validated = self.validate_article(article)
            validated_articles.append(validated)

            if validated["validation"]["approved"]:
                approved_count += 1
                status = "✅ 승인"
            else:
                status = "❌ 거부"

            print(
                f"[Validator] {i}/{len(articles)} {status}: {article['title'][:40]}"
            )

        # 승인된 뉴스만 필터링
        approved_articles = [
            article for article in validated_articles
            if article["validation"]["approved"]
        ]

        result = {
            "timestamp": datetime.now().isoformat(),
            "total_count": len(approved_articles),
            "validation_summary": {
                "processed": len(validated_articles),
                "approved": approved_count,
                "rejected": len(validated_articles) - approved_count,
                "approval_rate": approved_count / len(validated_articles) if validated_articles else 0
            },
            "articles": approved_articles
        }

        # 결과 저장
        output_file = self.workspace_dir / "validated_news.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"[Validator] 검증 완료")
        print(f"[Validator] 승인: {approved_count}/{len(validated_articles)}")
        print(f"[Validator] 결과 저장: {output_file}")

        return result


def run_skill() -> dict:
    """스킬 실행"""
    validator = NewsValidator()
    return validator.validate_all()


if __name__ == "__main__":
    result = run_skill()
    print("\n=== 검증 결과 ===")
    print(f"총 처리: {result['validation_summary']['processed']}개")
    print(f"승인됨: {result['validation_summary']['approved']}개")
    print(f"거부됨: {result['validation_summary']['rejected']}개")
    print(f"승인율: {result['validation_summary']['approval_rate']:.1%}")
