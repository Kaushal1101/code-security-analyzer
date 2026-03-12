from langgraph_workflow import build_graph


graph = build_graph()

initial_state = {
    "target_file": "./inputs/insecure_app.py",
    "vuln_type": "injection",
    "bandit_report_path": None,
    "semgrep_report_path": None,
    "parsed_report_path": None,
    "filtered_report_path": None,
    "llm_report_path": None,
    "has_findings": None
}

result = graph.invoke(initial_state)

print("\nFinal state:")
print(result)