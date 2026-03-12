# AI Code Security Analyzer

AI Code Security Analyzer is a lightweight security analysis pipeline that combines traditional static analysis tools with a local LLM to generate clear, human-readable vulnerability reports.

The goal is to bridge the gap between raw scanner output and actionable security documentation.

---

## Overview

The analyzer runs multiple security scanners, collects the findings, and feeds structured vulnerability data into a local LLM to generate a professional security report.

High level pipeline:

```text
Codebase
   ↓
Bandit + Semgrep
   ↓
Finding Normalization
   ↓
LLM Report Generation
   ↓
Markdown Security Report
```

---

## How the Workflow Works

1. **Static Analysis**
   - Bandit scans Python code for common security issues.
   - Semgrep runs security rules to detect vulnerable patterns.

2. **Finding Aggregation**
   - Results from Bandit and Semgrep are parsed.
   - High-severity findings are extracted.
   - Findings are normalized into a structured JSON format.

3. **LLM Prompt Generation**
   - The structured findings are injected into an LLM prompt.
   - The vulnerability type is explicitly passed to guide report writing.

4. **Report Generation**
   - A local LLM (via Ollama) generates a security report.
   - The report includes:
     - Executive summary
     - Vulnerability explanations
     - File locations
     - Severity
     - Recommended fixes

5. **Output**
   - The final report is saved as a Markdown document.

---

## Installation

### Install Python dependencies

```bash
pip install -r requirements.txt
```

This installs the Python packages used by the analyzer, including Bandit, Requests, and Semgrep.

### Install Ollama

Follow the official Ollama installation instructions for your operating system, then start the Ollama server:

```bash
ollama serve
```

### Pull the local model

```bash
ollama pull qwen3:4b
```

---

## Running the Analyzer

Run the main pipeline script:

```bash
python <entry_script>.py
```

Make sure the Ollama server is running before starting the analyzer.

After execution, the generated report will be saved to:

```text
reports/llm_report.md
```

---

## Example Use Case

1. Run the analyzer on a Python project.
2. Bandit and Semgrep identify vulnerabilities.
3. The findings are normalized.
4. The LLM generates a readable report explaining the issues and fixes.

This allows developers to quickly understand security problems without manually interpreting scanner outputs.

---

## Project Status

Prototype complete.

Planned improvements:

- VSCode extension integration
- Multi-language analysis support
- Expanded Semgrep rule coverage
- Interactive vulnerability triage