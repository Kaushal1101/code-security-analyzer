import json
from utils.parser import parse_reports as parse_reports_logic


def parse_reports(state: dict) -> dict:
    """
    LangGraph node that parses Bandit and Semgrep reports
    into an LLM-ready JSON.

    Reads:
        state["bandit_report_path"]
        state["semgrep_report_path"]

    Writes:
        state["parsed_report_path"]
        state["has_findings"]
    """

    output_path = parse_reports_logic(
        state["bandit_report_path"],
        state["semgrep_report_path"],
        "reports/parsed_report.json"
    )

    state["parsed_report_path"] = output_path

    # Determine if findings exist
    with open(output_path, "r") as f:
        parsed_data = json.load(f)

    state["has_findings"] = len(parsed_data) > 0

    return state