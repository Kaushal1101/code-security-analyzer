from typing import TypedDict


class GraphState(TypedDict):
    target_file: str
    bandit_report_path: str | None
    semgrep_report_path: str | None
    parsed_report_path: str | None
    llm_report_path: str | None
    has_finding: bool | None