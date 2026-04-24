import json
import os

REQUIREMENTS_PATH = "chosen_requirements.json"
EXPECTED_STRUCTURE_PATH = "expected_structure.json"
OUTPUT_PATH = "test_cases.json"

def generate_test_cases():
    with open(REQUIREMENTS_PATH, "r") as f:
        requirements = json.load(f)

    with open(EXPECTED_STRUCTURE_PATH, "r") as f:
        expected_structure = json.load(f)

    # Build lookup by requirement_id
    req_lookup = {r["requirement_id"]: r for r in requirements}

    # Validate expected structure matches requirements
    for parent_id, children in expected_structure.items():
        for child_letter in children:
            child_id = f"{parent_id}-{child_letter}"
            # Find matching requirement (ends with the letter suffix)
            match = next((r for r in requirements if r["requirement_id"] == f"{parent_id}{child_letter}"), None)
            if not match:
                print(f"WARNING: No requirement found for {parent_id}{child_letter}")

    test_cases = []
    tc_counter = 1

    for req in requirements:
        req_id = req["requirement_id"]
        description = req["description"]
        parent = req.get("parent", "N/A")
        source = req.get("source", "21 CFR 117.130")

        test_case = {
            "test_case_id": f"TC-{tc_counter:03d}",
            "requirement_id": req_id,
            "description": f"Verify that the system satisfies: {description}",
            "input_data": {
                "facility_type": "food manufacturing facility",
                "food_type": "ready-to-eat packaged food",
                "requirement_source": source,
                "parent_requirement": parent
            },
            "expected_output": {
                "status": "PASS",
                "compliance": True,
                "details": f"System demonstrates compliance with: {description}"
            },
            "steps": [
                f"1. Locate documentation relevant to {req_id} ({source}).",
                f"2. Verify the facility has addressed: {description}.",
                "3. Review written records or system task 1 outputs for evidence of compliance.",
                "4. Compare actual output against expected compliance state.",
                "5. Record PASS if compliant, FAIL with details if not."
            ],
            "notes": f"Derived from {source}, parent requirement: {parent}. Atomic rule: {req_id}."
        }

        test_cases.append(test_case)
        tc_counter += 1

    with open(OUTPUT_PATH, "w") as f:
        json.dump(test_cases, f, indent=2)

    print(f"Successfully generated {len(test_cases)} test cases -> {OUTPUT_PATH}")
    for tc in test_cases:
        print(f"  {tc['test_case_id']} | {tc['requirement_id']}")

if __name__ == "__main__":
    generate_test_cases()
