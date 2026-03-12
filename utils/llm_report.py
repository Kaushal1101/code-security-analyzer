import requests
import json
import time


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


def generate_llm_report(analysis_report_path: str, output_path: str, vuln_type: str) -> str:
    """
    Takes structured vulnerability analysis JSON and converts it
    into a polished Markdown security report using the LLM.

    Returns the output report path.
    """

    with open(analysis_report_path, "r") as f:
        analysis_data = json.load(f)

    analysis_json = json.dumps(analysis_data, indent=2)

    prompt = f"""
You are a cybersecurity report generator.

You are given structured vulnerability analysis data for the vulnerability type: {vuln_type}.

Your job is to convert this data into a professional Markdown security report.

Report requirements:
- Start with a report title
- Include a short executive summary describing the vulnerability type
- Clearly state the vulnerability type being analyzed
- Provide a section for each vulnerability instance
- Include file location and severity
- Clearly explain the issue and why it is dangerous
- Provide a recommended fix for each issue
- Include references if present

Structured analysis:
{analysis_json}

Generate a clean, well-structured Markdown report.
"""

    start = time.perf_counter()
    output = call_local_llm(prompt)
    end = time.perf_counter()

    elapsed = end - start

    with open(output_path, "w") as f:
        f.write(output)

    print(f"Markdown report generated ✅. Time taken: {elapsed:.2f} seconds.")

    return output_path
