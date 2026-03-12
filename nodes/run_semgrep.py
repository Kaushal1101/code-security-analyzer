import subprocess


def run_semgrep(state: dict) -> dict:
    """
    LangGraph node that runs Semgrep on the target file.

    Reads:
        state["target_file"]

    Writes:
        state["semgrep_report_path"]
    """

    target_file = state["target_file"]
    semgrep_report = "reports/semgrep_report.json"

    vuln_type = state.get("vuln_type")

    if vuln_type == "injection":
        configs = [
            "p/sql-injection",
            "p/xss",
            "p/command-injection",
        ]
    elif vuln_type == "unsafe_code_exec":
        configs = ["p/python"]
    elif vuln_type == "path_traversal":
        configs = ["p/security-audit"]
    elif vuln_type == "crypto_weakness":
        configs = ["p/security-audit"]
    else:
        configs = ["p/security-audit"]  # default fallback

    config_flags = " ".join([f"--config {c}" for c in configs])
    cmd = f"semgrep {config_flags} {target_file} --json -o {semgrep_report}"

    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)

    print(result.stdout)
    print(result.stderr)

    if result.returncode not in [0,1]:
        raise RuntimeError(f"Semgrep failed with exit code {result.returncode}")

    state["semgrep_report_path"] = semgrep_report

    return state