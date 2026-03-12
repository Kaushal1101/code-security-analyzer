import requests
import json
import time


def call_local_llm(prompt: str, model: str = "qwen3:4b") -> str:
    url = "http://localhost:11434/api/generate"

    payload = {
        "model": model,
        "prompt": prompt,
        "temperature": 0.2,
        "stream": False
    }

    response = requests.post(url, json=payload)

    if response.status_code != 200:
        raise Exception(f"LLM request failed: {response.text}")

    result = response.json()

    return result["response"]


def generate_llm_report(parsed_report_path: str, output_path: str) -> str:
    """
    Reads parsed findings and generates an LLM report.
    Returns the output report path.
    """

    with open(parsed_report_path, "r") as f:
        data = json.load(f)

    data = json.dumps(data, indent=2)

    prompt = f"""
You are given the following security findings:

{data}

Generate a human-readable security report with recommended fixes.
"""

    start = time.perf_counter()
    output = call_local_llm(prompt)
    end = time.perf_counter()

    elapsed = end - start

    with open(output_path, "w") as f:
        f.write(output)

    print(f"LLM report complete ✅. Time taken: {elapsed:.2f} seconds.")

    return output_path

'''
import requests
import json
import time

def call_local_llm(prompt: str, model: str = "qwen3:4b") -> str:

    url = "http://localhost:11434/api/generate"

    payload = {
        "model": model,
        "prompt": prompt,
        "temperature": 0.2,
        "stream": False
    }

    response = requests.post(url, json=payload)

    if response.status_code != 200:
        raise Exception(f"LLM request failed: {response.text}")

    result = response.json()

    return result["response"]

with open("/Users/kaushaljayapragash/Desktop/Cybersecurity/code-security-analyzer/reports/parsed_report.json", "r") as f:
    data = json.load(f)

data = json.dumps(data, indent=2)

prompt = f"""
You are given the following security findings:

    {data}

Generate a human-readable security report with recommended fixes.
"""

start = time.perf_counter()
output = call_local_llm(prompt)
end = time.perf_counter()

elapsed = end - start


with open("/Users/kaushaljayapragash/Desktop/Cybersecurity/code-security-analyzer/reports/final_report.md", "w") as f:
    data = f.write(output)

print(f"LLM report complete ✅. Time taken: {elapsed} seconds.")
'''