"""Render the checklist, source map, and README inventory from vulndb data."""

import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "vulndb" / "catalog.json"
SOURCE_MAP_PATH = ROOT / "vulndb" / "source-annotations.json"
CHECKLIST_PATH = ROOT / "vulndb" / "checklist.md"
IMPLEMENTATION_MAP_PATH = ROOT / "docs" / "implementation-map.md"
README_PATH = ROOT / "README.md"
INVENTORY_START = "<!-- BEGIN COMPLETE INVENTORY -->"
INVENTORY_END = "<!-- END COMPLETE INVENTORY -->"
ANNOTATIONS_START = "<!-- BEGIN MOVED ANNOTATIONS -->"
ANNOTATIONS_END = "<!-- END MOVED ANNOTATIONS -->"


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


def load_source_map():
    payload = json.loads(SOURCE_MAP_PATH.read_text(encoding="utf-8"))
    return {int(item_id): locations for item_id, locations in payload["ids"].items()}


def collect_source_refs():
    return load_source_map()


def render_implementation_map(catalog, source_refs=None):
    source_refs = collect_source_refs() if source_refs is None else source_refs
    entries = {row["id"]: row for row in catalog["entries"] if row["record_type"] == "vulnerability"}
    lines = [
        "# Source implementation map",
        "",
        "> Generated from the checked-in source map. The original inline annotations were moved to the README; this map keeps their symbol-level locations. A reference shows where a behavior is declared or implemented; it does not prove runtime reachability. Check `test_status` and the linked runtime/audit evidence separately.",
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


def render_readme_inventory(catalog):
    counts = catalog["counts"]
    lines = [
        INVENTORY_START,
        "## Complete inventory",
        "",
        "> Generated from `vulndb/catalog.json`. Every component and every numbered entry from the brief is listed here; the searchable version remains at `vulndb/index.html` and `vulndb/checklist.md`.",
        "",
        "### Application components",
        "",
        f"All **{counts['components']}** components, with implementation and test status.",
        "",
        "| ID | Component | Group | Type | Implementation | Test |",
        "|---:|---|---|---|---|---|",
    ]
    for row in catalog["components"]:
        lines.append(
            f"| {row['id']} | {cell(row['name'])} | {cell(row['category'])} | component | "
            f"{cell(row['implementation_status'])} | {cell(row['test_status'])} |"
        )
    lines.extend(
        [
            "",
            "### Numbered catalog",
            "",
            f"All **{counts['listed_entries']}** entries: {counts['vulnerabilities']} vulnerability topics, "
            f"{counts['attack_chains']} attack chains, and {counts['test_matrix_fields']} test-matrix fields.",
            "",
            "| ID | Name | Type | Group | Implementation | Test |",
            "|---:|---|---|---|---|---|",
        ]
    )
    for row in catalog["entries"]:
        lines.append(
            f"| {row['id']} | {cell(row['name'])} | {cell(row['record_type'])} | {cell(row['category'])} | "
            f"{cell(row['implementation_status'])} | {cell(row['test_status'])} |"
        )
    lines.append(INVENTORY_END)
    return "\n".join(lines) + "\n"


def render_readme_annotations(source_data):
    annotations = source_data["annotations"]
    lines = [
        ANNOTATIONS_START,
        "## Implementation notes moved out of source",
        "",
        "> The lab source no longer contains inline vulnerability hints. The following notes were moved here from source comments and docstrings, with the symbol that implements each behavior. Line-level evidence lives in `vulndb/source-annotations.json`; `docs/implementation-map.md` maps IDs to symbols.",
        "",
        f"**{len(annotations)}** notes covering **{len(source_data['ids'])}** vulnerability IDs.",
        "",
        "| File | Symbol | IDs | Original note |",
        "|---|---|---|---|",
    ]
    for item in annotations:
        ids = ", ".join(str(value) for value in item["ids"]) or "—"
        lines.append(
            f"| {cell(item['path'])} | {cell(item['symbol'])} | {ids} | {cell(item['note'])} |"
        )
    lines.append(ANNOTATIONS_END)
    return "\n".join(lines) + "\n"


def replace_readme_section(text, start_marker, end_marker, replacement):
    start = text.index(start_marker)
    end = text.index(end_marker) + len(end_marker)
    return text[:start] + replacement.rstrip("\n") + text[end:]


def render_readme(readme_text, catalog, source_data):
    text = replace_readme_section(
        readme_text, INVENTORY_START, INVENTORY_END, render_readme_inventory(catalog)
    )
    return replace_readme_section(
        text, ANNOTATIONS_START, ANNOTATIONS_END, render_readme_annotations(source_data)
    )


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
    source_data = json.loads(SOURCE_MAP_PATH.read_text(encoding="utf-8"))
    CHECKLIST_PATH.write_text(render(catalog), encoding="utf-8", newline="\n")
    IMPLEMENTATION_MAP_PATH.write_text(render_implementation_map(catalog), encoding="utf-8", newline="\n")
    readme = README_PATH.read_text(encoding="utf-8")
    README_PATH.write_text(render_readme(readme, catalog, source_data), encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
