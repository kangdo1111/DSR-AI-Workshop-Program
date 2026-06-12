"""
issue-writer 스킬: GitHub 이슈 자동 생성

Coordinator Agent가 사용하는 스킬입니다.
분석 결과를 바탕으로 GitHub 이슈를 자동 생성합니다.
"""

import json
import os
from pathlib import Path
from datetime import datetime

# GitHub API는 실제 프로젝트에서 PyGithub이나 requests로 구현
# 여기서는 문제점을 JSON으로 저장하는 방식으로 구현


class IssueWriter:
    """GitHub 이슈 자동 생성"""

    def __init__(self):
        self.workspace_dir = Path("/workspace/data")
        self.workspace_dir.mkdir(parents=True, exist_ok=True)

    def extract_issues(self, articles: list[dict]) -> list[dict]:
        """뉴스에서 이슈 추출"""
        issues = []
        issue_id = 1

        for article in articles:
            analysis = article.get("analysis", {})

            # 기술적 영향도가 High인 뉴스만 이슈로
            if analysis.get("technical_impact") != "High":
                continue

            # 주요 이슈가 있는 경우만
            key_issues = analysis.get("key_issues", [])
            if not key_issues:
                continue

            for key_issue in key_issues:
                issue = {
                    "id": issue_id,
                    "title": f"[{analysis.get('category', '기타')}] {key_issue[:60]}",
                    "body": self._format_issue_body(article, key_issue, analysis),
                    "labels": [
                        "news-analysis",
                        analysis.get("category", "기타").lower(),
                        analysis.get("technical_impact", "Unknown").lower(),
                        "auto-generated"
                    ],
                    "priority": "high" if analysis.get("market_impact") == "High" else "medium",
                    "source_article": article.get("title", ""),
                    "source_url": article.get("url", ""),
                    "created_at": datetime.now().isoformat()
                }
                issues.append(issue)
                issue_id += 1

        return issues

    def _format_issue_body(self, article: dict, issue: str, analysis: dict) -> str:
        """GitHub 이슈 본문 포맷팅"""
        body = f"""## 📋 이슈 개요

**원본 뉴스**: [{article.get('title', 'N/A')}]({article.get('url', '#')})

## 🔍 분석

**카테고리**: {analysis.get('category', '기타')}
**기술 영향도**: {analysis.get('technical_impact', 'Unknown')}
**시장 영향도**: {analysis.get('market_impact', 'Unknown')}

## 📌 핵심 이슈

{issue}

## 📝 상세 분석

{analysis.get('summary', 'N/A')}

## 📚 출처

{analysis.get('source_citation', 'N/A')}

---
**자동 생성**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**생성 시스템**: News Automation Harness v1.0
"""
        return body

    def create_issues(self, issues: list[dict]) -> dict:
        """이슈 생성 (시뮬레이션)"""
        print(f"[IssueWriter] {len(issues)}개 이슈 생성 시작...")

        created_issues = []
        for issue in issues:
            print(f"[IssueWriter] 이슈 생성: {issue['title'][:50]}")
            # 실제로는 GitHub API 호출
            # response = gh.get_user().get_repo("DSR-AI-Workshop-Program").create_issue(...)
            # 여기서는 JSON으로 저장
            created_issues.append({
                **issue,
                "github_id": f"GH#{1000 + issue['id']}",
                "status": "created"
            })

        return created_issues

    def run(self) -> dict:
        """전체 이슈 작성 파이프라인"""
        # 분석된 뉴스 읽기
        input_file = self.workspace_dir / "analyzed_news.json"

        if not input_file.exists():
            print("[IssueWriter] 분석된 뉴스를 찾을 수 없습니다.")
            return {"status": "error", "issues_count": 0}

        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        articles = data.get("articles", [])

        # 이슈 추출
        issues = self.extract_issues(articles)
        print(f"[IssueWriter] {len(issues)}개 이슈 추출됨")

        if not issues:
            print("[IssueWriter] 생성할 이슈가 없습니다.")
            return {
                "status": "no_issues",
                "issues_count": 0,
                "message": "기술 영향도가 High이고 주요 이슈가 있는 뉴스가 없습니다."
            }

        # 이슈 생성
        created_issues = self.create_issues(issues)

        result = {
            "status": "success",
            "issues_count": len(created_issues),
            "issues": created_issues,
            "created_at": datetime.now().isoformat(),
            "message": f"{len(created_issues)}개의 GitHub 이슈가 생성되었습니다."
        }

        # 결과 저장
        output_file = self.workspace_dir / "created_issues.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"[IssueWriter] 이슈 생성 완료: {output_file}")

        return result


def run_skill() -> dict:
    """스킬 실행"""
    writer = IssueWriter()
    return writer.run()


if __name__ == "__main__":
    result = run_skill()
    print("\n=== 이슈 작성 결과 ===")
    print(f"상태: {result.get('status')}")
    print(f"생성된 이슈: {result.get('issues_count')}개")
