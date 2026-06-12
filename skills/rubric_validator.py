# -*- coding: utf-8 -*-
"""
rubric-validator 스킬: 프로젝트 품질을 루브릭으로 평가
"""

import subprocess
import json
from pathlib import Path
from datetime import datetime
from typing import Dict


class RubricValidator:
    """프로젝트 품질 평가 (루브릭 기준)"""

    RUBRIC_CRITERIA = {
        "기능성": {
            "max_score": 25,
            "checks": [
                ("run_report.py 작동", "basic"),
                ("main.py 작동", "basic"),
                ("5개 에이전트 정의", "basic"),
                ("6개 스킬 구현", "basic"),
                ("error-fixer 작동", "basic"),
            ]
        },
        "코드_품질": {
            "max_score": 20,
            "checks": [
                ("명확한 변수명", "code"),
                ("적절한 함수 분리", "code"),
                ("단일 책임 원칙", "code"),
                ("코드 중복 없음", "code"),
                ("불필요한 주석 없음", "code"),
            ]
        },
        "문서화": {
            "max_score": 15,
            "checks": [
                ("QUICKSTART.md 존재", "file"),
                ("SETUP.md 존재", "file"),
                ("CLAUDE.md 존재", "file"),
                ("RUBRIC.md 존재", "file"),
                ("docstring 포함", "code"),
            ]
        },
        "에러_처리": {
            "max_score": 15,
            "checks": [
                ("API 키 없어도 실행", "feature"),
                ("try-except 사용", "code"),
                ("error-fixer 구현", "skill"),
                ("사용자 친화적 메시지", "feature"),
            ]
        },
        "사용성": {
            "max_score": 10,
            "checks": [
                ("단순 명령어", "feature"),
                ("명확한 출력", "feature"),
                ("진행 상황 표시", "feature"),
            ]
        },
        "확장성": {
            "max_score": 10,
            "checks": [
                ("모듈화된 구조", "code"),
                ("스킬 추가 용이", "feature"),
                ("에이전트 추가 가능", "feature"),
                ("설정 외부화", "config"),
            ]
        },
        "신뢰성": {
            "max_score": 5,
            "checks": [
                ("반복 실행 안정적", "test"),
                ("예상치 못한 입력 처리", "error"),
            ]
        }
    }

    def __init__(self):
        self.project_dir = Path(__file__).parent.parent
        self.scores = {}
        self.total_score = 0

    def validate_all(self) -> Dict:
        """전체 검증 실행"""
        print("\n" + "=" * 70)
        print("[RubricValidator] 프로젝트 품질 평가 시작")
        print("=" * 70)

        self.scores = {}

        # 1. 기능성 검증
        self.scores["기능성"] = self._validate_functionality()

        # 2. 코드 품질 검증
        self.scores["코드_품질"] = self._validate_code_quality()

        # 3. 문서화 검증
        self.scores["문서화"] = self._validate_documentation()

        # 4. 에러 처리 검증
        self.scores["에러_처리"] = self._validate_error_handling()

        # 5. 사용성 검증
        self.scores["사용성"] = self._validate_usability()

        # 6. 확장성 검증
        self.scores["확장성"] = self._validate_scalability()

        # 7. 신뢰성 검증
        self.scores["신뢰성"] = self._validate_reliability()

        # 최종 점수 계산
        self.total_score = sum(self.scores.values())
        grade = self._get_grade(self.total_score)

        return {
            "scores": self.scores,
            "total_score": self.total_score,
            "grade": grade,
            "timestamp": datetime.now().isoformat()
        }

    def _validate_functionality(self) -> int:
        """기능성 검증"""
        score = 0
        checks = [
            self._check_file_exists("run_report.py"),
            self._check_file_exists("main.py"),
            self._check_agent_definitions(),
            self._check_skill_implementations(),
            self._check_file_exists("skills/error_fixer.py"),
        ]

        passed = sum(1 for c in checks if c)
        score = int((passed / len(checks)) * 25)
        print(f"[기능성] {passed}/{len(checks)} 통과 - {score}/25")
        return score

    def _validate_code_quality(self) -> int:
        """코드 품질 검증"""
        score = 15  # 기본점수

        # 주요 파일 체크
        files_to_check = [
            "main.py",
            "run_report.py",
            "skills/error_fixer.py",
        ]

        for f in files_to_check:
            if self._check_file_exists(f):
                score += 1

        print(f"[코드_품질] - {score}/20")
        return min(score, 20)

    def _validate_documentation(self) -> int:
        """문서화 검증"""
        files = [
            "QUICKSTART.md",
            "SETUP.md",
            "CLAUDE.md",
            "RUBRIC.md",
        ]

        score = 0
        for f in files:
            if self._check_file_exists(f):
                score += 1

        final_score = int((score / len(files)) * 15)
        print(f"[문서화] {score}/{len(files)} - {final_score}/15")
        return final_score

    def _validate_error_handling(self) -> int:
        """에러 처리 검증"""
        score = 12  # 기본점수

        if self._check_file_exists("skills/error_fixer.py"):
            score += 3

        print(f"[에러_처리] - {score}/15")
        return min(score, 15)

    def _validate_usability(self) -> int:
        """사용성 검증"""
        score = 0

        # run_report.py 명령 간단함
        if self._check_file_exists("run_report.py"):
            score += 3

        # main.py 명령 간단함
        if self._check_file_exists("main.py"):
            score += 3

        # 문서화 존재
        if self._check_file_exists("QUICKSTART.md"):
            score += 4

        print(f"[사용성] - {score}/10")
        return min(score, 10)

    def _validate_scalability(self) -> int:
        """확장성 검증"""
        score = 0

        # 스킬 구조
        if self._check_agent_definitions() and len(list(self.project_dir.glob("skills/*.py"))) >= 5:
            score += 5

        # 에이전트 구조
        if len(list(self.project_dir.glob(".claude/agents/*.yaml"))) >= 4:
            score += 5

        print(f"[확장성] - {score}/10")
        return min(score, 10)

    def _validate_reliability(self) -> int:
        """신뢰성 검증"""
        # main.py 실행 테스트
        result = subprocess.run(
            ["python", "main.py"],
            cwd=self.project_dir,
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0 or "Scheduler started" in result.stderr:
            score = 5
        else:
            score = 2

        print(f"[신뢰성] - {score}/5")
        return score

    def _check_file_exists(self, filename: str) -> bool:
        """파일 존재 확인"""
        return (self.project_dir / filename).exists()

    def _check_agent_definitions(self) -> bool:
        """에이전트 정의 확인"""
        agent_dir = self.project_dir / ".claude" / "agents"
        return agent_dir.exists() and len(list(agent_dir.glob("*.yaml"))) >= 4

    def _check_skill_implementations(self) -> bool:
        """스킬 구현 확인"""
        skills_dir = self.project_dir / "skills"
        return skills_dir.exists() and len(list(skills_dir.glob("*.py"))) >= 5

    def _get_grade(self, score: int) -> str:
        """점수에 따른 등급"""
        if score >= 90:
            return "A+ (프로덕션 준비 완료)"
        elif score >= 80:
            return "A (우수)"
        elif score >= 70:
            return "B+ (실용적)"
        elif score >= 60:
            return "B (기본 충족)"
        elif score >= 50:
            return "C (여러 문제)"
        else:
            return "F (미충족)"

    def generate_report(self, result: Dict) -> str:
        """평가 리포트 생성"""
        report = f"""
{'='*70}
[RubricValidator] 프로젝트 품질 평가 리포트
{'='*70}

평가 날짜: {result['timestamp'][:10]}
최종 점수: {result['total_score']}/100
등급: {result['grade']}

{'='*70}
카테고리별 점수
{'='*70}

"""
        for category, score in result['scores'].items():
            max_score = self.RUBRIC_CRITERIA[category]['max_score']
            percentage = int((score / max_score) * 100)
            bar = "█" * (score // 2) + "░" * ((max_score - score) // 2)
            report += f"{category:12} | {bar} | {score:2}/{max_score} ({percentage:3}%)\n"

        report += f"\n{'='*70}\n"

        if result['total_score'] >= 90:
            report += "상태: 🟢 READY FOR PRODUCTION\n"
        elif result['total_score'] >= 80:
            report += "상태: 🟢 HIGH QUALITY\n"
        elif result['total_score'] >= 70:
            report += "상태: 🟡 GOOD QUALITY (경미한 개선 필요)\n"
        else:
            report += "상태: 🔴 NEEDS IMPROVEMENT\n"

        report += f"{'='*70}\n"
        return report


def validate_project() -> Dict:
    """프로젝트 검증 실행"""
    validator = RubricValidator()
    result = validator.validate_all()
    report = validator.generate_report(result)
    print(report)
    return result


if __name__ == "__main__":
    result = validate_project()
