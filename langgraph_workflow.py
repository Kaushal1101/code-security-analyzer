from langgraph.graph import StateGraph, END

from state import GraphState

from nodes.run_bandit import run_bandit
from nodes.run_semgrep import run_semgrep
from nodes.parse_reports import parse_reports
from nodes.filter_findings import filter_findings
from nodes.generate_llm_report import generate_llm_report
from nodes.no_findings_report import no_findings_report
from nodes.llm_analyze_findings import llm_analyze_findings

def route_after_filter(state):
    if state.get("has_findings"):
        return "llm_analyze_findings"
    return "no_findings_report"


def build_graph():

    workflow = StateGraph(GraphState)

    workflow.add_node("run_bandit", run_bandit)
    workflow.add_node("run_semgrep", run_semgrep)
    workflow.add_node("parse_reports", parse_reports)
    workflow.add_node("filter_findings", filter_findings)
    workflow.add_node("generate_llm_report", generate_llm_report)
    workflow.add_node("no_findings_report", no_findings_report)
    workflow.add_node("llm_analyze_findings", llm_analyze_findings)

    workflow.set_entry_point("run_bandit")

    workflow.add_edge("run_bandit", "run_semgrep")
    workflow.add_edge("run_semgrep", "parse_reports")
    workflow.add_edge("parse_reports", "filter_findings")
    workflow.add_conditional_edges(
        "filter_findings",
        route_after_filter,
        {
            "llm_analyze_findings": "llm_analyze_findings",
            "no_findings_report": "no_findings_report",
        }
    )
    workflow.add_edge("llm_analyze_findings", "generate_llm_report")
    workflow.add_edge("generate_llm_report", END)
    workflow.add_edge("no_findings_report", END)

    return workflow.compile()