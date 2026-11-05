"""Render the human-readable checklist from vulndb/catalog.json."""

import json
import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "vulndb" / "catalog.json"
CHECKLIST_PATH = ROOT / "vulndb" / "checklist.md"
IMPLEMENTATION_MAP_PATH = ROOT / "docs" / "implementation-map.md"
SOURCE_ROOTS = (ROOT / "backend", ROOT / "frontend", ROOT / "services")
VULN_REFERENCE = re.compile(r"#\s*(\d+)")


def cell(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


def evidence_link(row):
    links = []
    implementation = row.get("implementation_evidence")
    evidence = row.get("evidence")
    if implementation:
        links.append(f"Source: [{cell(implementation)}]({cell(implementation)})")
    if evidence:
        links.append(f"Test/audit: [{cell(evidence)}]({cell(evidence)})")
    return " · ".join(links) if links else "—"


def collect_source_refs():
    refs = defaultdict(set)
    for source_root in SOURCE_ROOTS:
        for path in source_root.rglob("*"):
            if path.suffix not in {".py", ".js"} or "node_modules" in path.parts or "__pycache__" in path.parts:
                continue
            relative = path.relative_to(ROOT).as_posix()
            for line_number, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
                if "vuln" not in line.lower():
                    continue
                for match in VULN_REFERENCE.finditer(line):
                    if re.match(r"\s*-\s*\d+", line[match.end():]):
                        continue
                    item_id = int(match.group(1))
                    if 1 <= item_id <= 661:
                        refs[item_id].add(f"{relative}:{line_number}")
    return {item_id: sorted(locations) for item_id, locations in sorted(refs.items())}


def render_implementation_map(catalog, source_refs=None):
    source_refs = collect_source_refs() if source_refs is None else source_refs
    entries = {row["id"]: row for row in catalog["entries"] if row["record_type"] == "vulnerability"}
    lines = [
        "# Source implementation map",
        "",
        "> Generated from explicit vulnerability annotations in the lab source. A source reference shows where a behavior is declared or implemented; it does not prove runtime reachability. Check `test_status` and the linked runtime/audit evidence separately.",
        "",
        f"Annotated vulnerability IDs: **{len(source_refs)} / {len(entries)}**.",
        "",
        "| ID | Vulnerability | Annotated source locations |",
        "|---:|---|---|",
    ]
    for item_id, locations in source_refs.items():
        row = entries.get(item_id)
        if row:
            references = ", ".join(f"`{cell(location)}`" for location in locations)
            lines.append(f"| {item_id} | {cell(row['name'])} | {references} |")
    return "\n".join(lines) + "\n"


def render(catalog):
    counts = catalog["counts"]
    lines = [
        "# VulnShop coverage checklist",
        "",
        "> The inventory preserves all IDs and names from the supplied brief. `observed` implementation status means source, runtime, or dependency evidence is recorded; `verified` test status requires runtime or audit evidence. The source map is not proof of runtime reachability. See linked evidence in the final column.",
        "",
        "## Counts",
        "",
        "| Scope | Count |",
        "|---|---:|",
        f"| Application components | {counts['components']} |",
        f"| Vulnerability entries | {counts['vulnerabilities']} |",
        f"| Attack-chain scenarios | {counts['attack_chains']} |",
        f"| Test-matrix fields | {counts['test_matrix_fields']} |",
        f"| Total entries in the 1–726 list | {counts['listed_entries']} |",
        "",
        "## Application components",
        "",
        "| ID | Component | Group | Implementation | Test | Evidence |",
        "|---:|---|---|---|---|---|",
    ]
    for row in catalog["components"]:
        lines.append(
            f"| {row['id']} | {cell(row['name'])} | {cell(row['category'])} | "
            f"{cell(row['implementation_status'])} | {cell(row['test_status'])} | {evidence_link(row)} |"
        )

    grouped = defaultdict(list)
    category_order = []
    for row in catalog["entries"]:
        category = row["category"]
        if category not in grouped:
            category_order.append(category)
        grouped[category].append(row)

    for category in category_order:
        lines.extend(
            [
                "",
                f"## {category}",
                "",
                "| ID | Name | Type | Implementation | Test | Evidence |",
                "|---:|---|---|---|---|---|",
            ]
        )
        for row in grouped[category]:
            lines.append(
                f"| {row['id']} | {cell(row['name'])} | {cell(row['record_type'])} | "
                f"{cell(row['implementation_status'])} | {cell(row['test_status'])} | {evidence_link(row)} |"
            )
    return "\n".join(lines) + "\n"


def main():
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    CHECKLIST_PATH.write_text(render(catalog), encoding="utf-8", newline="\n")
    IMPLEMENTATION_MAP_PATH.write_text(render_implementation_map(catalog), encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
