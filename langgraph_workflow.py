from langgraph.graph import StateGraph, END

from state import GraphState

from nodes.run_bandit import run_bandit
from nodes.run_semgrep import run_semgrep
from nodes.parse_reports import parse_reports
from nodes.generate_llm_report import generate_llm_report
from nodes.no_findings_report import no_findings_report


def route_after_parse(state):
    if state.get("has_findings"):
        return "generate_llm_report"
    return "no_findings_report"


def build_graph():

    workflow = StateGraph(GraphState)

    workflow.add_node("run_bandit", run_bandit)
    workflow.add_node("run_semgrep", run_semgrep)
    workflow.add_node("parse_reports", parse_reports)
    workflow.add_node("generate_llm_report", generate_llm_report)
    workflow.add_node("no_findings_report", no_findings_report)

    workflow.set_entry_point("run_bandit")

    workflow.add_edge("run_bandit", "run_semgrep")
    workflow.add_edge("run_semgrep", "parse_reports")
    workflow.add_conditional_edges(
        "parse_reports",
        route_after_parse,
        {
            "generate_llm_report": "generate_llm_report",
            "no_findings_report": "no_findings_report",
        }
    )
    workflow.add_edge("generate_llm_report", END)
    workflow.add_edge("no_findings_report", END)

    return workflow.compile()