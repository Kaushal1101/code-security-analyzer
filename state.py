from typing import TypedDict


class GraphState(TypedDict):
    target_file: str
    vuln_type: str | None
    bandit_report_path: str | None
    semgrep_report_path: str | None
    parsed_report_path: str | None
    filtered_report_path: str | None
    llm_report_path: str | None
    has_findings: bool | None
    analysis_report_path: str | None