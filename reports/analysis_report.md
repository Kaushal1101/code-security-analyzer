{
  "vuln_type": "Command Injection",
  "total_findings": 2,
  "high_priority_findings": 1,
  "findings": [
    {
      "title": "Subprocess call with shell=True in inputs/insecure_app.py (line 27)",
      "vuln_family": "Command Injection",
      "file": "inputs/insecure_app.py",
      "line": 27,
      "severity": "ERROR",
      "confidence": "MEDIUM",
      "root_cause": "Using shell=True in subprocess.call without proper input sanitization",
      "impact": "Allows arbitrary command injection, enabling malicious actors to execute shell commands",
      "exploit_scenario": "An attacker can inject arbitrary shell commands by manipulating the input string",
      "recommended_fix": "Change the call to use shell=False and ensure the command string is properly sanitized",
      "references": [
        "https://stackoverflow.com/questions/3172470/actual-meaning-of-shell-true-in-subprocess",
        "https://docs.python.org/3/library/subprocess.html"
      ]
    },
    {
      "title": "Subprocess call with shell=True in inputs/insecure_app.py (line 27)",
      "vuln_family": "Command Injection",
      "file": "././inputs/insecure_app.py",
      "line": 27,
      "severity": "HIGH",
      "confidence": "HIGH",
      "root_cause": "Using shell=True in subprocess.call without proper input sanitization",
      "impact": "Allows arbitrary command injection, enabling malicious actors to execute shell commands",
      "exploit_scenario": "An attacker can inject arbitrary shell commands by manipulating the input string",
      "recommended_fix": "Change the call to use shell=False and ensure the command string is properly sanitized",
      "references": []
    }
  ]
}