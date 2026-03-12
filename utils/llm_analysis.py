import json
import requests


SYSTEM_PROMPT = """You are a cybersecurity assistant.

You are given structured findings from static analysis tools.
Your job is to analyze them and return structured JSON only.

Rules:
- Only analyze the provided findings.
- Do not invent vulnerabilities not supported by the findings.
- Focus only on the specified vulnerability family.
- Keep explanations concise and practical.
- If a finding is weak or ambiguous, say so clearly.
- Output valid JSON only. Do not include markdown fences or extra text.
"""


JSON_SCHEMA_HINT = {
    "summary": {
        "vuln_type": "string",
        "total_findings": 0,
        "high_priority_findings": 0,
    },
    "analyzed_findings": [
        {
            "title": "string",
            "vuln_family": "string",
            "file": "string",
            "line": 0,
            "severity": "string",
            "confidence": "string or null",
            "root_cause": "string",
            "impact": "string",
            "exploit_scenario": "string",
            "recommended_fix": "string",
            "references": ["string"]
        }
    ]
}


def call_local_llm(prompt: str, model: str = "qwen3:4b") -> str:
    url = "http://localhost:11434/api/generate"

    payload = {
        "model": model,
        "prompt": prompt,
        "temperature": 0.2,
        "stream": False,
    }

    response = requests.post(url, json=payload)

    if response.status_code != 200:
        raise Exception(f"LLM request failed: {response.text}")

    result = response.json()
    return result["response"]


def _load_findings(filtered_report_path: str) -> list[dict]:
    with open(filtered_report_path, "r") as f:
        return json.load(f)


def _trim_findings_for_prompt(findings: list[dict]) -> list[dict]:
    trimmed = []

    for finding in findings:
        trimmed.append(
            {
                "tool": finding.get("tool"),
                "rule_id": finding.get("rule_id"),
                "file": finding.get("file") or finding.get("filename"),
                "line": finding.get("line") or finding.get("line_number"),
                "severity": finding.get("severity"),
                "confidence": finding.get("confidence"),
                "message": finding.get("message") or finding.get("issue_text"),
                "cwe": finding.get("cwe") or finding.get("CWE"),
                "category": finding.get("category"),
                "vulnerability_class": finding.get("vulnerability_class"),
                "code_snippet": finding.get("code_snippet"),
                "references": finding.get("references"),
                "source": finding.get("source"),
            }
        )

    return trimmed


def _build_prompt(findings: list[dict], vuln_type: str) -> str:
    trimmed_findings = _trim_findings_for_prompt(findings)
    findings_json = json.dumps(trimmed_findings, indent=2)
    schema_json = json.dumps(JSON_SCHEMA_HINT, indent=2)

    return f"""{SYSTEM_PROMPT}

Vulnerability family: {vuln_type}

Return JSON in this shape:
{schema_json}

Findings:
{findings_json}
"""


def analyze_findings(filtered_report_path: str, vuln_type: str, output_path: str, model: str = "qwen3:4b") -> str:
    """
    Reads filtered findings, sends them to the local LLM for structured analysis,
    and writes the resulting JSON analysis to output_path.

    Returns:
        output_path
    """

    findings = _load_findings(filtered_report_path)

    prompt = _build_prompt(findings, vuln_type)
    llm_output = call_local_llm(prompt, model=model)

    try:
        analyzed_data = json.loads(llm_output)
    except json.JSONDecodeError as e:
        raise ValueError(
            "LLM output was not valid JSON. "
            f"Raw output:\n{llm_output}"
        ) from e

    with open(output_path, "w") as f:
        json.dump(analyzed_data, f, indent=2)

    return output_path