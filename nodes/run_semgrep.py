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

    cmd = f"semgrep --config p/security-audit {target_file} --json -o {semgrep_report}"

    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)

    print(result.stdout)
    print(result.stderr)

    if result.returncode not in [0,1]:
        raise RuntimeError(f"Semgrep failed with exit code {result.returncode}")

    state["semgrep_report_path"] = semgrep_report

    return state