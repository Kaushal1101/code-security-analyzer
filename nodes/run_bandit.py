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

    vuln_type = state.get("vuln_type")

    if vuln_type == "injection":
        tests = "B102,B307,B602,B605"  # exec/eval/subprocess injection
    elif vuln_type == "unsafe_code_exec":
        tests = "B102,B307"  # exec/eval
    elif vuln_type == "path_traversal":
        tests = "B301,B302"  # unsafe file handling / pickle
    elif vuln_type == "crypto_weakness":
        tests = "B303,B304,B305"  # weak crypto / hashes
    else:
        tests = None

    if tests:
        cmd = f"bandit -t {tests} {target_file} --exit-zero -f json -o {bandit_report}"
    else:
        cmd = f"bandit {target_file} --exit-zero -f json -o {bandit_report}"

    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)

    print(result.stdout)
    print(result.stderr)

    if result.returncode not in [0]:
        raise RuntimeError(f"Bandit failed with exit code {result.returncode}")

    state["bandit_report_path"] = bandit_report

    return state