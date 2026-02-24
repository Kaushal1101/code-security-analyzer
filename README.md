Notice:
- Outer fence = **four backticks**
- Inner fences = **three backticks**

---

## ✅ Here Is Your Properly Wrapped README

Copy everything below exactly:

````markdown
# AI Code Security Analyzer

An AI-powered static analysis tool that combines traditional security scanners with a local LLM to generate human-readable vulnerability reports.

This prototype integrates:

- **Bandit** – Python security linter  
- **Semgrep** – Static analysis with security-focused rules  
- **Local LLM (via Ollama)** – Generates structured remediation reports  

The tool scans code, filters high-severity findings, and produces a professional Markdown security report with recommended fixes.

---

## How It Works

1. Run static analysis using Bandit and Semgrep  
2. Normalize and filter high-severity findings  
3. Inject structured findings into an LLM prompt  
4. Generate a human-readable security report  
5. Save output as a Markdown file  

Pipeline flow:

```
Code → Bandit + Semgrep → Normalize → LLM → report.md
```

---

## Installation

### 1. Install Dependencies

```bash
pip install bandit
brew install semgrep
brew install ollama
```

### 2. Download LLM Model

```bash
ollama pull llama2.3:3b
```

Start Ollama:

```bash
ollama serve
```

---

## Usage

Run the full pipeline:

```bash
python your_script_name.py
```

The generated report will be saved to:

```
reports/llm_report.md
```

---

## Project Status

✅ End-to-end prototype complete  

🚧 Planned Improvements:
- VSCode extension integration  
- Project-wide analysis mode  
- Automated test case generation  
