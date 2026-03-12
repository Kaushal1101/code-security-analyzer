

import time


def no_findings_report(state: dict) -> dict:
    """
    LangGraph node that writes a simple report when no findings are detected.

    Reads:
        state["parsed_report_path"] (optional)

    Writes:
        state["llm_report_path"]
    """

    output_path = "reports/final_report.md"

    report = """
# Security Analysis Report

## Summary

No security findings were detected by Bandit or Semgrep for the scanned file.

This does not guarantee the code is completely secure, but no issues were flagged by the current static analysis rules.

## Tools Used

- Bandit (Python security linter)
- Semgrep (static analysis engine)

"""

    with open(output_path, "w") as f:
        f.write(report)

    print("No findings detected. Report generated.")

    state["llm_report_path"] = output_path

    return state