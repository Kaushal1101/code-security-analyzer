import subprocess


def run_bandit(state: dict) -> dict:
    """
    LangGraph node that runs Bandit on the target file.
    Reads:
        state["target_file"]

    Writes:
        state["bandit_report_path"]
    """

    target_file = state["target_file"]
    bandit_report = "reports/bandit_report.json"

    cmd = f"bandit {target_file} --exit-zero -f json -o {bandit_report}"

    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)

    print(result.stdout)
    print(result.stderr)

    if result.returncode not in [0]:
        raise RuntimeError(f"Bandit failed with exit code {result.returncode}")

    state["bandit_report_path"] = bandit_report

    return state