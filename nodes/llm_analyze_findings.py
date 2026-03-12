from utils.llm_analysis import analyze_findings as analyze_findings_logic


def llm_analyze_findings(state: dict) -> dict:
    """
    LangGraph node that analyzes the findings using an LLM.

    Reads:
        state["filtered_report_path"]

    Writes:
        state["analysis_report_path"]
    """

    output_path = analyze_findings_logic(
        state["filtered_report_path"],
        state["vuln_type"],
        "reports/analysis_report.md"
    )

    state["analysis_report_path"] = output_path

    return state