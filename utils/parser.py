import json

def parse_semgrep_result(raw: dict) -> dict:
    start = raw.get("start", {})
    extra = raw.get("extra", {})
    metadata = extra.get("metadata", {})

    parsed = {
        "tool": "semgrep",
        "rule_id": raw.get("check_id"),
        "file": raw.get("path"),
        "line": start.get("line"),
        "column": start.get("col"),
        "severity": extra.get("severity"),
        "confidence": metadata.get("confidence"),
        "message": extra.get("message"),
        "cwe": metadata.get("cwe"),
        "owasp": metadata.get("owasp"),
        "category": metadata.get("category"),
        "vulnerability_class": metadata.get("vulnerability_class"),
        "references": metadata.get("references"),
        "source": metadata.get("source"),
    }

    return parsed


def parse_reports(bandit_path: str, semgrep_path: str, output_path: str) -> str:
    # Bandit
    with open(bandit_path, "r") as f:
        data = json.load(f)

    delete_list = ["col_offset", "end_col_offset", "line_range"]
    rename_dict = {
        "code": "code_snippet",
        "issue_confidence": "confidence",
        "issue_severity": "severity",
        "issue_cwe": "CWE",
        "issue_text": "message"
    }

    for result in data["results"]:
        for key in delete_list:
            result.pop(key, None)

        result["tool"] = "bandit"

        for old_key, new_key in rename_dict.items():
            if old_key in result:
                result[new_key] = result.pop(old_key)

    bandit_data = data["results"]


    # Semgrep
    with open(semgrep_path, "r") as f:
        data = json.load(f)

    results = []

    for result in data["results"]:
        parsed = parse_semgrep_result(result)
        results.append(parsed)

    semgrep_data = results

    # Combine
    all_data = semgrep_data + bandit_data

    with open(output_path, "w") as f:
        json.dump(all_data, f, indent=2)

    return output_path

