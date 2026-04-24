import json
import re
import argparse
from collections import defaultdict

# ---------- Arguments ----------
parser = argparse.ArgumentParser(description="Generate requirement JSON from CFR Markdown")
parser.add_argument("--input", "-i", required=True, help="Input Markdown file (.md)")
parser.add_argument("--output", "-o", required=True, help="Output JSON file")
parser.add_argument("--cfr", "-c", required=True, help="CFR section (e.g., 21 CFR 117.130)")
parser.add_argument("--structure", "-s", required=True, help="Output expected structure JSON file")
args = parser.parse_args()

INPUT_MD = args.input
OUTPUT_JSON = args.output
CFR_SECTION = args.cfr
STRUCTURE_JSON = args.structure

# ---------- Read File ----------
with open(INPUT_MD, "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

# ---------- Parse ----------
raw = []
has_subatomic = set()
parent_descriptions = {}
current_req = None
current_subsection = None

for line in lines:
    req_match = re.search(r"\u2192\s*(REQ-[\d\.]+-\d+)", line)
    if req_match:
        current_req = req_match.group(1)
        current_subsection = None
        continue

    subsection_match = re.match(r"^-?\s*\((\d+)\)", line)
    if subsection_match and current_req and not re.search(r"\u2192", line):
        current_subsection = subsection_match.group(1)
        continue

    atomic_match = re.match(r"^(.*?)\s*\u2192\s*([A-Z]\d*)$", line)
    if atomic_match and current_req:
        description = atomic_match.group(1).strip()
        description = re.sub(r"^(\([ivxlcdmIVXLCDM]+\)\s*|[^a-zA-Z])+", "", description).strip()
        suffix = atomic_match.group(2)
        base_req = f"{current_req}-{current_subsection}" if current_subsection else current_req
        parent_key = f"{base_req}{suffix[0]}"

        if len(suffix) == 1:
            parent_descriptions[f"{base_req}{suffix}"] = description
        else:
            has_subatomic.add(parent_key)

        raw.append((base_req, suffix, description))

# ---------- Generate Requirements ----------
requirements = []
expected_structure = defaultdict(list)

for base_req, suffix, description in raw:
    parent_key = f"{base_req}{suffix[0]}"

    if len(suffix) == 1:
        if parent_key in has_subatomic:
            continue
        requirements.append({
            "requirement_id": f"{base_req}{suffix}",
            "description": description,
            "source": CFR_SECTION,
            "parent": base_req
        })
        expected_structure[base_req].append(suffix)
    else:
        requirement_id = f"{parent_key}{chr(64 + int(suffix[1:]))}"
        full_description = f"{parent_descriptions[parent_key]}; {description}" if parent_key in has_subatomic else description
        requirements.append({
            "requirement_id": requirement_id,
            "description": full_description,
            "source": CFR_SECTION,
            "parent": parent_key
        })
        expected_structure[parent_key].append(chr(64 + int(suffix[1:])))

# ---------- Save Requirements ----------
with open(OUTPUT_JSON, "w") as f:
    json.dump(requirements, f, indent=2)
print(f"Saved {len(requirements)} requirements → {OUTPUT_JSON}")

# ---------- Save Expected Structure ----------
with open(STRUCTURE_JSON, "w") as f:
    items = list(expected_structure.items())
    lines_out = ["{"]
    for i, (parent, suffixes) in enumerate(items):
        comma = "," if i < len(items) - 1 else ""
        lines_out.append(f'  "{parent}": {json.dumps(suffixes)}{comma}')
    lines_out.append("}")
    f.write("\n".join(lines_out))
print(f"Saved expected structure ({len(expected_structure)} parents) → {STRUCTURE_JSON}")