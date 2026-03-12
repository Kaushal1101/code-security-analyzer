from utils.llm_report import generate_llm_report as generate_llm_report_logic


def generate_llm_report(state: dict) -> dict:
    """
    LangGraph node that generates the final LLM report.

    Reads:
        state["analysis_report_path"]

    Writes:
        state["llm_report_path"]
    """

    output_path = generate_llm_report_logic(
        state["analysis_report_path"],
        state["vuln_type"],
        "reports/final_report.md"
    )

    state["llm_report_path"] = output_path

    return state