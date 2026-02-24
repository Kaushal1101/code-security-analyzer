import requests
import json

def call_local_llm(prompt: str, model: str = "llama3.2:3b") -> str:

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


with open("reports/parsed_report.json", "r") as f:
    data = json.load(f)

data = json.dumps(data, indent=2)

prompt = f"""
You are given the following security findings:

    {data}

Generate a human-readable security report with recommended fixes.
"""

output = call_local_llm(prompt)
print(output)
