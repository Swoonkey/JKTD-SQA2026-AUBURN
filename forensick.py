# forensick.py
# Task 4: Forensick Integration – 5 forensic methods for V&V traceability

import json
from datetime import datetime

LOG_FILE = "forensick_log.txt"

def log(message):
    """Write a timestamped message to the forensick log file and print it."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {message}"
    print(entry)
    with open(LOG_FILE, "a") as f:
        f.write(entry + "\n")

# M1: Log timestamp when forensick run begins
def log_run_start():
    log("=== FORENSICK RUN STARTED ===")

# M2: Check for missing requirements in test_cases.json
def check_missing_requirements(requirements_path="requirements.json",
                                test_cases_path="test_cases.json"):
    log("METHOD 2: Checking for requirements missing from test cases...")
    try:
        with open(requirements_path) as f:
            requirements = json.load(f)
        with open(test_cases_path) as f:
            test_cases = json.load(f)
    except FileNotFoundError as e:
        log(f"  ERROR: Could not open file - {e}")
        return

    req_ids = {r["requirement_id"] for r in requirements}
    tested_ids = {tc["requirement_id"] for tc in test_cases}
    missing = req_ids - tested_ids

    if missing:
        for m in sorted(missing):
            log(f"  MISSING: Requirement '{m}' has no test case.")
    else:
        log("  OK: All requirements have at least one test case.")

# M3: Check for skipped requirements in expected_structure.json
def check_skipped_requirements(expected_path="expected_structure.json",
                                test_cases_path="test_cases.json"):
    log("METHOD 3: Checking for requirements skipped in expected structure...")
    try:
        with open(expected_path) as f:
            expected = json.load(f)
        with open(test_cases_path) as f:
            test_cases = json.load(f)
    except FileNotFoundError as e:
        log(f"  ERROR: Could not open file - {e}")
        return

    expected_ids = set(expected.keys())
    tested_ids = {tc["requirement_id"] for tc in test_cases}
    skipped = expected_ids - tested_ids

    if skipped:
        for s in sorted(skipped):
            log(f"  SKIPPED: '{s}' is in expected_structure but has no test case.")
    else:
        log("  OK: No skipped requirements detected.")

# M4: Validate required fields in every test case
def check_test_case_completeness(test_cases_path="test_cases.json"):
    log("METHOD 4: Validating completeness of test case fields...")
    required_fields = ["test_case_id", "requirement_id", "description",
                       "input_data", "expected_output"]
    try:
        with open(test_cases_path) as f:
            test_cases = json.load(f)
    except FileNotFoundError as e:
        log(f"  ERROR: Could not open file - {e}")
        return

    all_ok = True
    for tc in test_cases:
        for field in required_fields:
            if field not in tc or not tc[field]:
                log(f"  INCOMPLETE: Test case '{tc.get('test_case_id','?')}' "
                    f"is missing field '{field}'.")
                all_ok = False
    if all_ok:
        log("  OK: All test cases have the required fields.")

# M5: Log overall forensick summary and CI-style pass/fail
def log_summary(requirements_path="requirements.json",
                test_cases_path="test_cases.json"):
    log("METHOD 5: Generating forensick summary report...")
    try:
        with open(requirements_path) as f:
            requirements = json.load(f)
        with open(test_cases_path) as f:
            test_cases = json.load(f)
    except FileNotFoundError as e:
        log(f"  ERROR: Could not open file - {e}")
        log("  CI BUILD STATUS: FAILED")
        return

    req_ids = {r["requirement_id"] for r in requirements}
    tested_ids = {tc["requirement_id"] for tc in test_cases}
    coverage = len(tested_ids & req_ids) / len(req_ids) * 100 if req_ids else 0

    log(f"  Total requirements : {len(req_ids)}")
    log(f"  Requirements tested: {len(tested_ids & req_ids)}")
    log(f"  Coverage           : {coverage:.1f}%")

    if coverage >= 80:
        log("  CI BUILD STATUS: PASSED")
    else:
        log("  CI BUILD STATUS: FAILED (coverage below 80%)")

    log("=== FORENSICK RUN COMPLETE ===")

# Entry point
if __name__ == "__main__":
    log_run_start()
    check_missing_requirements()
    check_skipped_requirements()
    check_test_case_completeness()
    log_summary()