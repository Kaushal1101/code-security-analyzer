bandit insecure_app.py -f json -o reports/bandit_report.json
semgrep --config p/security-audit insecure_app.py --json -o reports/semgrep_report.json
python scripts/parser.py
python scripts/test_llm.py
