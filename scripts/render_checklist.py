"""Render the human-readable checklist from vulndb/catalog.json."""

import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "vulndb" / "catalog.json"
CHECKLIST_PATH = ROOT / "vulndb" / "checklist.md"


def cell(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


def evidence_link(row):
    evidence = row.get("evidence")
    return f"[{cell(evidence)}]({cell(evidence)})" if evidence else "—"


def render(catalog):
    counts = catalog["counts"]
    lines = [
        "# VulnShop coverage checklist",
        "",
        "> The inventory preserves all IDs and names from the supplied brief. Statuses change only when direct runtime or audit evidence is recorded; entries without evidence remain unverified. See the evidence documents linked in the final column.",
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


if __name__ == "__main__":
    main()
