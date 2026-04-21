# SQA Project Report
**Team:** Jase Schwanke, Krish Modi, Ty Mullinx, Drew Black  



### Task 1 – Jase Schwanke
We parsed through '21_CFR_117.130.md' regulatory document and selected 10 atomic rules. These were then encoded in 'requirements.json', with each entry containing a 'requirement_id', description, source, and parent field for better traceability. We produced 'expected_structure.json', which maps each parent requirement ID to the expected child letter suffixes. This required careful reading of the CFR text to correctly assign letters and ignore numbering errors in the source document.

### Task 2 – Krish Modi
We wrote `generate_test_cases.py` to consume `requirements.json` and `expected_structure.json` and produce `test_cases.json`. Each test case was structured with a unique `test_case_id`, a linked `requirement_id`, a description of what is being verified, structured `input_data`, an `expected_output` block, step-by-step test instructions, and traceability notes back to the source regulation. One test case was generated per requirement.

### Task 3 – Jase Schwanke, Drew Black
We implemented two separate scripts:

- **`verify.py`** (Verification): Checks that all requirements conform to structural rules — required fields are present, requirement IDs match a defined regex format (`REQ-[\w\.]+-\d{3}[A-Z]{1,2}`), each requirement has at least one test case, descriptions avoid vague language, and parent-child ID relationships are consistent.
- **`validate.py`** (Validation): Checks completeness against the `expected_structure.json` spec — every expected child requirement exists in `requirements.json`, and no unexpected requirements appear under a mapped parent.

Both scripts exit with code `1` on failure so that the GitHub Actions CI pipeline reports a failed build. We tested both the passing and failing states and captured screenshots of each outcome.

### Task 4 – Ty Mullinx, Drew Black
We integrated Forensick into five points across the V&V scripts and CI workflow to capture forensic evidence of quality events. The five integration points were:

1. **Requirement skipped/missing** — when `validate.py` detects a missing child requirement, a Forensick event is logged with the missing requirement ID and the parent context.
2. **Unexpected requirement detected** — when `validate.py` finds a requirement not listed in `expected_structure.json`, a Forensick event flags it as an unapproved addition.
3. **Verification rule failure** — when `verify.py` fails any structural rule (bad ID format, missing field, vague description, parent-child mismatch), the specific failure message is forwarded to Forensick for audit trail purposes.
4. **No test case for requirement** — when `verify.py` finds a requirement with no corresponding test case, a Forensick event is emitted to record the traceability gap.
5. **CI build pass/fail** — the GitHub Actions workflow emits a Forensick event at the end of each run recording the overall build outcome (pass or fail), the triggering branch, and the commit SHA.

This gave us a persistent, queryable forensic log of every quality failure across the project's lifecycle, independent of the CI run logs.



## What We Learned
**Regulatory document parsing:** CFR documents use inconsistent formatting that does not map cleanly to code. Extracting atomic, independently testable units required careful manual review alongside scripted parsing, and taught us the importance of validating parser output against source material.

**Atomic requirement decomposition:** A single regulatory section like 21 CFR 117.130 contains many overlapping obligations. Decomposing it into atomic rules — each independently verifiable — forced us to be precise about scope and avoid combining two requirements into one test case.

**Verification vs. Validation:** These terms are often conflated. This project made the distinction concrete:
- *Verification* asks whether the artifact conforms to its own rules and format (internal consistency).
- *Validation* asks whether the artifact matches an external specification (did we capture the right requirements?).

**Traceability:** Enforcing that every requirement has a test case (in `verify.py`) and that every expected requirement exists (in `validate.py`) gave us hands-on experience with traceability matrices — a core SQA practice in regulated industries.

**CI as a quality gate:** Wiring the scripts into GitHub Actions showed how automated checks prevent regressions. A broken requirement structure or missing test case fails the build immediately rather than being caught late or not at all.

**Structured data design:** Designing consistent JSON schemas across `requirements.json`, `expected_structure.json`, and `test_cases.json` demonstrated how data contract discipline enables tools to be composed — the output of one script becomes the verified input to the next.

**Forensic logging:** Integrating Forensick taught us that CI pass/fail alone is insufficient for regulated software — you need a durable, tamper-evident record of *what* failed, *when*, and *where* in the pipeline. Choosing meaningful integration points (not just wrapping everything) required us to think about which quality events actually matter for an audit.
