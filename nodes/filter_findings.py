import json


KEYWORD_MAP = {
    "injection": ["injection", "sql", "shell=true", "subprocess", "command"],
    "unsafe_code_exec": ["eval", "exec", "pickle", "deserialization", "yaml.load"],
    "path_traversal": ["path traversal", "directory traversal", "../", "file path", "open("],
    "crypto_weakness": ["md5", "sha1", "weak cryptography", "weak hash", "hardcoded key"],
}


def filter_findings(state: dict) -> dict:
    """
    LangGraph node that filters parsed findings by vulnerability family.

    Reads:
        state["parsed_report_path"]
        state["vuln_type"]

    Writes:
        state["filtered_report_path"]
        state["has_findings"]
    """

    parsed_report_path = state["parsed_report_path"]
    vuln_type = state.get("vuln_type")
    output_path = "reports/filtered_report.json"

    with open(parsed_report_path, "r") as f:
        findings = json.load(f)

    if not vuln_type or vuln_type not in KEYWORD_MAP:
        filtered = findings
    else:
        keywords = KEYWORD_MAP[vuln_type]
        filtered = []

        for finding in findings:
            combined_text = " ".join(
                str(finding.get(key, ""))
                for key in [
                    "message",
                    "rule_id",
                    "category",
                    "cwe",
                    "CWE",
                    "code_snippet",
                    "vulnerability_class",
                ]
            ).lower()

            if any(keyword in combined_text for keyword in keywords):
                filtered.append(finding)

    with open(output_path, "w") as f:
        json.dump(filtered, f, indent=2)

    state["filtered_report_path"] = output_path
    state["has_findings"] = len(filtered) > 0

    return state