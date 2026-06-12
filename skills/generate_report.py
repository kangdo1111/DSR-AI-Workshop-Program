"""
generate-report 스킬: HTML 리포트 생성

Reporter Agent가 사용하는 메인 스킬입니다.
검증된 뉴스로부터 전문적인 HTML 리포트를 생성합니다.
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from jinja2 import Environment, FileSystemLoader, Template


class ReportGenerator:
    """HTML 리포트 생성"""

    HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>자동차 스프링 업계 뉴스 분석 리포트</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', 'Noto Sans KR', sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
        }
        .container { max-width: 1000px; margin: 0 auto; padding: 20px; }
        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            border-radius: 8px;
            margin-bottom: 40px;
        }
        h1 { font-size: 2.5em; margin-bottom: 10px; }
        .date-range { font-size: 1.1em; opacity: 0.9; }
        .summary {
            background: white;
            padding: 30px;
            border-radius: 8px;
            margin-bottom: 40px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .summary h2 { color: #667eea; margin-bottom: 15px; }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        .stat-box {
            background: #f9f9f9;
            padding: 15px;
            border-left: 4px solid #667eea;
            border-radius: 4px;
        }
        .stat-number { font-size: 2em; font-weight: bold; color: #667eea; }
        .stat-label { color: #666; margin-top: 5px; }
        .articles {
            display: grid;
            gap: 20px;
            margin-bottom: 40px;
        }
        .article-card {
            background: white;
            padding: 25px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-left: 4px solid #667eea;
        }
        .article-card h3 {
            color: #667eea;
            margin-bottom: 10px;
            font-size: 1.3em;
        }
        .article-meta {
            display: flex;
            gap: 20px;
            font-size: 0.9em;
            color: #666;
            margin-bottom: 15px;
        }
        .badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: bold;
            margin: 5px 5px 5px 0;
        }
        .badge-tech { background: #e3f2fd; color: #1976d2; }
        .badge-market { background: #f3e5f5; color: #7b1fa2; }
        .badge-high { background: #ffebee; color: #c62828; }
        .badge-medium { background: #fff3e0; color: #e65100; }
        .badge-low { background: #e8f5e9; color: #2e7d32; }
        .article-summary {
            margin: 15px 0;
            padding: 15px;
            background: #f9f9f9;
            border-radius: 4px;
            border-left: 3px solid #ddd;
        }
        .article-link {
            display: inline-block;
            margin-top: 10px;
            padding: 8px 16px;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 4px;
            font-size: 0.9em;
        }
        .article-link:hover { background: #764ba2; }
        .issues-section {
            background: white;
            padding: 30px;
            border-radius: 8px;
            margin-bottom: 40px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .issues-section h2 { color: #667eea; margin-bottom: 20px; }
        .issue {
            padding: 15px;
            margin-bottom: 10px;
            background: #f9f9f9;
            border-left: 4px solid #764ba2;
            border-radius: 4px;
        }
        .issue-category { font-weight: bold; color: #764ba2; }
        footer {
            text-align: center;
            padding: 20px;
            color: #999;
            font-size: 0.9em;
            border-top: 1px solid #ddd;
            margin-top: 40px;
        }
        .toc {
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 40px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .toc h3 { color: #667eea; margin-bottom: 15px; }
        .toc ul { list-style: none; }
        .toc li { margin: 8px 0; }
        .toc a { color: #667eea; text-decoration: none; }
        .toc a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📰 자동차 스프링 업계 뉴스 분석</h1>
            <div class="date-range">{{ date_range }}</div>
        </header>

        <div class="toc">
            <h3>📋 Contents</h3>
            <ul>
                <li><a href="#summary">Executive Summary</a></li>
                <li><a href="#articles">주요 뉴스</a></li>
                <li><a href="#issues">핵심 이슈</a></li>
                <li><a href="#sources">출처</a></li>
            </ul>
        </div>

        <div class="summary" id="summary">
            <h2>Executive Summary</h2>
            <div class="stats">
                <div class="stat-box">
                    <div class="stat-number">{{ articles|length }}</div>
                    <div class="stat-label">분석 뉴스</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">{{ high_impact_count }}</div>
                    <div class="stat-label">High Impact</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">{{ categories|length }}</div>
                    <div class="stat-label">이슈 카테고리</div>
                </div>
            </div>
            <p style="margin-top: 20px; padding: 15px; background: #f9f9f9; border-radius: 4px;">
                이번 주 {{ date_range }}에 수집된 {{ articles|length }}개의 뉴스 중,
                {{ high_impact_count }}개가 산업에 높은 영향도를 미치는 것으로 분석되었습니다.
                주요 이슈는 기술 혁신, 정책 변화, 시장 경쟁 등 다양한 분야에 걸쳐 있습니다.
            </p>
        </div>

        <div class="articles" id="articles">
            <h2>주요 뉴스</h2>
            {% for article in articles %}
            <div class="article-card">
                <h3>{{ article.title }}</h3>
                <div class="article-meta">
                    <span>📅 {{ article.date[:10] }}</span>
                    <span>📰 {{ article.source }}</span>
                </div>
                <div style="margin: 15px 0;">
                    {% if article.analysis.technical_impact == 'High' %}
                        <span class="badge badge-tech">기술</span>
                        <span class="badge badge-high">{{ article.analysis.technical_impact }}</span>
                    {% elif article.analysis.technical_impact == 'Medium' %}
                        <span class="badge badge-tech">기술</span>
                        <span class="badge badge-medium">{{ article.analysis.technical_impact }}</span>
                    {% else %}
                        <span class="badge badge-tech">기술</span>
                        <span class="badge badge-low">{{ article.analysis.technical_impact }}</span>
                    {% endif %}
                    <span class="badge badge-market">카테고리: {{ article.analysis.category }}</span>
                </div>
                <div class="article-summary">
                    <strong>전문가 분석:</strong><br>
                    {{ article.analysis.summary }}
                </div>
                {% if article.analysis.key_issues %}
                <div style="margin: 10px 0;">
                    <strong>주요 이슈:</strong>
                    <ul style="margin-left: 20px; margin-top: 8px;">
                    {% for issue in article.analysis.key_issues %}
                        <li>{{ issue }}</li>
                    {% endfor %}
                    </ul>
                </div>
                {% endif %}
                {% if article.analysis.source_citation %}
                <div style="margin-top: 10px; font-size: 0.9em; color: #666;">
                    {{ article.analysis.source_citation }}
                </div>
                {% endif %}
                <a href="{{ article.url }}" class="article-link" target="_blank">원문 읽기 →</a>
            </div>
            {% endfor %}
        </div>

        {% if issues %}
        <div class="issues-section" id="issues">
            <h2>🔴 핵심 이슈</h2>
            {% for category, items in issues.items() %}
            <div style="margin-bottom: 20px;">
                <h3 style="color: #764ba2; margin-bottom: 10px;">{{ category }}</h3>
                {% for item in items %}
                <div class="issue">
                    {{ item }}
                </div>
                {% endfor %}
            </div>
            {% endfor %}
        </div>
        {% endif %}

        <div class="summary" id="sources">
            <h2>📚 출처</h2>
            <ul style="list-style-position: inside;">
            {% for source in sources %}
                <li style="margin: 8px 0;">{{ source }}</li>
            {% endfor %}
            </ul>
        </div>

        <footer>
            <p>📊 자동차 스프링 업계 뉴스 자동화 시스템</p>
            <p>생성일: {{ generated_at }}</p>
            <p>© 2026 DSR-AI-Workshop-Program</p>
        </footer>
    </div>
</body>
</html>"""

    def __init__(self):
        self.workspace_dir = Path("/workspace/data")
        self.workspace_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir = Path("output/reports")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def categorize_issues(self, articles: list[dict]) -> dict:
        """뉴스에서 이슈 추출 및 분류"""
        issues = {}

        for article in articles:
            analysis = article.get("analysis", {})
            category = analysis.get("category", "기타")

            if category not in issues:
                issues[category] = []

            for issue in analysis.get("key_issues", []):
                issues[category].append(issue)

        return issues

    def generate(self) -> dict:
        """리포트 생성"""
        # 검증된 뉴스 읽기
        input_file = self.workspace_dir / "validated_news.json"

        if not input_file.exists():
            print("[Reporter] 검증된 뉴스 파일을 찾을 수 없습니다.")
            return {"status": "error", "message": "No validated news found"}

        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        articles = data.get("articles", [])
        print(f"[Reporter] {len(articles)}개 뉴스로 리포트 생성 중...")

        # 이슈 분류
        issues = self.categorize_issues(articles)

        # 통계 계산
        high_impact_count = sum(
            1 for article in articles
            if article.get("analysis", {}).get("technical_impact") == "High"
        )

        # 날짜 범위 계산
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        date_range = f"{week_start.strftime('%Y.%m.%d')}~{week_end.strftime('%Y.%m.%d')}"

        # 출처 목록
        sources = sorted(set(article.get("source", "") for article in articles))

        # Jinja2 렌더링
        template = Template(self.HTML_TEMPLATE)
        html = template.render(
            articles=articles,
            issues=issues,
            date_range=date_range,
            high_impact_count=high_impact_count,
            categories=issues.keys(),
            sources=sources,
            generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        # 파일 저장
        report_filename = f"report_{datetime.now().strftime('%Y%m%d')}.html"
        report_path = self.output_dir / report_filename
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"[Reporter] 리포트 생성 완료: {report_path}")

        result = {
            "status": "success",
            "report_path": str(report_path),
            "articles_count": len(articles),
            "issues_count": sum(len(v) for v in issues.values()),
            "high_impact_count": high_impact_count,
            "generated_at": datetime.now().isoformat(),
            "date_range": date_range
        }

        # 메타데이터 저장
        metadata_file = self.workspace_dir / "report_metadata.json"
        with open(metadata_file, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"[Reporter] 메타데이터 저장: {metadata_file}")

        return result


def run_skill() -> dict:
    """스킬 실행"""
    generator = ReportGenerator()
    return generator.generate()


if __name__ == "__main__":
    result = run_skill()
    print("\n=== 리포트 생성 결과 ===")
    print(f"상태: {result.get('status')}")
    print(f"경로: {result.get('report_path')}")
    print(f"뉴스: {result.get('articles_count')}개")
    print(f"이슈: {result.get('issues_count')}개")
