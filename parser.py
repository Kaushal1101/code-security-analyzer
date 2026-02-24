import json
import pprint

with open("reports/bandit_report.json", "r") as f:
    data = json.load(f)

delete_list = ["col_offset", "end_col_offset", "line_range"]
rename_dict = {"code": "code_snippet", 
               "issue_confidence": "confidence", 
               "issue_severity": "severity",
               "issue_cwe": "CWE",
               "issue_info": "message"
               }


for result in data["results"]:
    for key in delete_list:
        result.pop(key, None)
    
    result["tool"] = "bandit"

    for old_key, new_key in rename_dict.items():
        if old_key in result:
            result[new_key] = result.pop(old_key)

    


## pprint.pprint(data["results"][0])

bandit_data = data["results"]

    
with open("reports/semgrep_report.json", "r") as f:
    data = json.load(f)


def parse_semgrep_result(raw: dict) -> dict:
    """
    Takes ONE semgrep result object (not the entire JSON file)
    and returns a simplified LLM-ready dictionary.
    """

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


results = []

for result in data["results"]:
    parsed = parse_semgrep_result(result)
    results.append(parsed)

semgrep_data = results

all_data = semgrep_data + bandit_data


with open("reports/parsed_report.json", "w") as f:
    json.dump(all_data, f, indent=2)


#pprint.pprint(all_data)

