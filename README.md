# SQA Project

**Team:** Jase Schwanke, Krish Modi, Ty Mullinx, Drew Black

## Overview

This project implements a Software Quality Assurance (SQA) pipeline for the FDA regulation **21 CFR 117.130** (Hazard Analysis). The pipeline parses a regulatory Markdown document, generates structured requirements and test cases, and runs automated verification and validation checks via GitHub Actions CI.

### Project Objectives

1. Parse CFR regulatory text into machine-readable requirements (`requirements.json`)
2. Generate structured test cases from those requirements (`test_cases.json`)
3. Verify internal consistency of requirements (ID format, required fields, traceability)
4. Validate completeness against an expected structure spec (`expected_structure.json`)
5. Capture forensic evidence of quality events via Forensick integration
6. Automate all checks in a GitHub Actions CI pipeline

## Repository Structure

```
SQA/
├── CFR-117.130.md              # Source regulatory document
├── generate_requirements.py    # Task 1 – parses CFR doc → requirements.json + expected_structure.json
├── generate_test_cases.py      # Task 2 – consumes requirements → test_cases.json
├── verify.py                   # Task 3 – verification (internal consistency checks)
├── validate.py                 # Task 3 – validation (completeness against expected_structure.json)
├── forensick.py                # Task 4 – Forensick forensic event integration
├── requirements.json           # Generated requirements
├── expected_structure.json     # Expected parent-child requirement structure
├── test_cases.json             # Generated test cases
└── .github/workflows/ci.yml   # GitHub Actions CI pipeline
```

## Prerequisites

- Python 3.11+
- Git

No external Python packages are required beyond the standard library.

## Reproducing Locally

### Clone the Repository

```bash
git clone <repo-url>
cd SQA
```

### Windows

```powershell
# Generate requirements and expected structure from CFR document
python generate_requirements.py -i CFR-117.130.md -o requirements.json -c "21 CFR 117.130" -s expected_structure.json

# Generate test cases
python generate_test_cases.py

# Run validation (completeness check)
python validate.py

# Run verification (structural consistency check)
python verify.py

# Run Forensick integration
python forensick.py
```

### Mac / Linux

```bash
# Generate requirements and expected structure from CFR document
python3 generate_requirements.py -i CFR-117.130.md -o requirements.json -c "21 CFR 117.130" -s expected_structure.json

# Generate test cases
python3 generate_test_cases.py

# Run validation (completeness check)
python3 validate.py

# Run verification (structural consistency check)
python3 verify.py

# Run Forensick integration
python3 forensick.py
```

Both `verify.py` and `validate.py` exit with code `1` on failure, which causes the CI pipeline to report a failed build.

## CI Pipeline

GitHub Actions runs automatically on every push or pull request to `main`. The workflow:

1. Checks out the repository
2. Sets up Python 3.11
3. Runs `validate.py`
4. Runs `verify.py`
5. Runs `forensick.py`

See `.github/workflows/ci.yml` for the full configuration.
