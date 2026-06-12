# -*- coding: utf-8 -*-
"""
error-fixer 스킬: 프로젝트 에러를 자동으로 감지하고 수정
"""

import subprocess
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List


class ErrorFixer:
    """프로젝트 에러 자동 수정"""

    ERROR_FIXES = {
        "ModuleNotFoundError: No module named": {
            "name": "패키지 미설치",
            "solution": "pip_install",
            "pattern": r"No module named '([^']+)'",
        },
        "ModuleNotFoundError: No module named 'cgi'": {
            "name": "Python 3.14 호환성",
            "solution": "remove_anthropic_import",
            "files_to_fix": ["skills/analyze_ai.py"],
        },
    }

    def __init__(self):
        self.project_dir = Path(__file__).parent.parent
        self.log_dir = self.project_dir / "logs"
        self.log_dir.mkdir(exist_ok=True)

    def run_project(self, script: str = "main.py", timeout: int = 30) -> Dict:
        """프로젝트 실행"""
        print(f"[ErrorFixer] {script} 실행 중...")

        try:
            result = subprocess.run(
                ["python", script],
                cwd=self.project_dir,
                capture_output=True,
                text=True,
                timeout=timeout
            )

            if result.returncode != 0:
                return {
                    "status": "error",
                    "error_output": result.stderr + result.stdout,
                    "script": script,
                }
            else:
                return {
                    "status": "success",
                    "output": result.stdout,
                    "script": script
                }

        except subprocess.TimeoutExpired:
            return {"status": "timeout", "script": script}
        except Exception as e:
            return {"status": "exception", "error": str(e)}

    def analyze_error(self, error_output: str) -> Dict:
        """에러 분석"""
        print("[ErrorFixer] 에러 분석 중...")

        analysis = {
            "error_type": "Unknown",
            "error_message": "",
            "fix_available": False,
            "suggested_fix": None,
        }

        for error_pattern, fix_info in self.ERROR_FIXES.items():
            if error_pattern in error_output:
                analysis["error_type"] = fix_info["name"]
                analysis["fix_available"] = True
                analysis["suggested_fix"] = fix_info["solution"]
                break

        return analysis

    def fix_error(self, analysis: Dict) -> Dict:
        """에러 수정"""
        print(f"[ErrorFixer] {analysis['error_type']} 수정 중...")

        fix_result = {
            "status": "unknown",
            "fix_type": analysis["suggested_fix"],
        }

        if analysis["suggested_fix"] == "remove_anthropic_import":
            files_to_fix = self.ERROR_FIXES.get(
                "ModuleNotFoundError: No module named 'cgi'", {}
            ).get("files_to_fix", [])

            for file_path in files_to_fix:
                full_path = self.project_dir / file_path
                if full_path.exists():
                    self._remove_anthropic_lines(full_path)
                    fix_result["status"] = "success"

        return fix_result

    def _remove_anthropic_lines(self, file_path: Path) -> bool:
        """Anthropic import 제거"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            filtered_lines = []
            for line in lines:
                if "from anthropic" not in line and "client = Anthropic" not in line:
                    filtered_lines.append(line)

            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(filtered_lines)

            return True
        except Exception as e:
            print(f"[ErrorFixer] 파일 수정 실패: {str(e)}")
            return False

    def run_full_cycle(self, script: str = "main.py") -> Dict:
        """전체 사이클 (실행-분석-수정-검증)"""
        print("\n" + "="*70)
        print("[ErrorFixer] 에러 감지 및 자동 수정")
        print("="*70)

        # 1단계: 실행
        run_result = self.run_project(script)

        if run_result["status"] == "success":
            print("[OK] 성공!")
            return {
                "final_status": "success",
                "message": "프로젝트가 정상적으로 작동합니다."
            }

        # 2단계: 분석
        analysis = self.analyze_error(run_result.get("error_output", ""))
        print(f"[ERROR] {analysis['error_type']}")

        if not analysis["fix_available"]:
            print("[WARNING] 자동 수정 불가 - 수동 검토 필요")
            return {
                "final_status": "manual_review_needed",
                "error_type": analysis["error_type"]
            }

        # 3단계: 수정
        fix_result = self.fix_error(analysis)

        if fix_result["status"] == "success":
            print("[OK] 수정 완료")

        # 4단계: 검증
        verify_result = self.run_project(script)

        return {
            "final_status": verify_result["status"],
            "message": "에러 수정 완료" if verify_result["status"] == "success" else "수정 후에도 에러 존재"
        }


if __name__ == "__main__":
    fixer = ErrorFixer()
    result = fixer.run_full_cycle("main.py")
    print(f"\n[RESULT] {result}")
