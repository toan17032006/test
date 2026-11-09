import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.render_checklist import (
    ANNOTATIONS_END,
    ANNOTATIONS_START,
    INVENTORY_END,
    INVENTORY_START,
    collect_source_refs,
    render,
    render_implementation_map,
    render_readme,
)


class CatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = json.loads((ROOT / "vulndb" / "catalog.json").read_text(encoding="utf-8"))

    def test_component_ids_and_count_are_complete(self):
        components = self.catalog["components"]
        self.assertEqual(len(components), 275)
        self.assertEqual([row["id"] for row in components], list(range(1, 276)))
        self.assertTrue(all(row["category"] and row["name"] for row in components))
        verified = [row for row in components if row["test_status"] == "verified"]
        self.assertTrue(verified)
        for row in verified:
            self.assertEqual(row["implementation_status"], "observed", row["id"])
            self.assertEqual(row.get("evidence"), "docs/component-smoke.md", row["id"])
            self.assertTrue((ROOT / row["evidence"]).is_file())
        self.assertTrue(all(row["implementation_status"] == "unverified" for row in components if row["test_status"] == "not_tested"))

    def test_component_smoke_report_lists_every_verified_component(self):
        expected = {row["id"] for row in self.catalog["components"] if row.get("evidence") == "docs/component-smoke.md"}
        report = (ROOT / "docs" / "component-smoke.md").read_text(encoding="utf-8")
        documented = set()
        in_table = False
        for line in report.splitlines():
            if line.startswith("| IDs"):
                in_table = True
                continue
            if in_table and not line.startswith("|"):
                break
            if not in_table or line.startswith("|---"):
                continue
            documented.update(int(value.strip()) for value in line.split("|")[1].split(","))
        self.assertEqual(documented, expected)

    def test_all_726_listed_entries_are_preserved_once(self):
        entries = self.catalog["entries"]
        self.assertEqual(len(entries), 726)
        self.assertEqual([row["id"] for row in entries], list(range(1, 727)))
        self.assertTrue(all(row["category"] and row["name"] for row in entries))

    def test_record_types_match_the_source_ranges(self):
        entries = self.catalog["entries"]
        self.assertEqual(sum(row["record_type"] == "vulnerability" for row in entries), 661)
        self.assertEqual(sum(row["record_type"] == "attack_chain" for row in entries), 29)
        self.assertEqual(sum(row["record_type"] == "test_matrix_field" for row in entries), 36)
        self.assertTrue(all(row["record_type"] == "vulnerability" for row in entries[:661]))
        self.assertTrue(all(row["record_type"] == "attack_chain" for row in entries[661:690]))
        self.assertTrue(all(row["record_type"] == "test_matrix_field" for row in entries[690:]))

    def test_dependency_findings_have_auditable_evidence(self):
        entries = {row["id"]: row for row in self.catalog["entries"]}
        for item_id in (543, 544, 618):
            self.assertEqual(entries[item_id]["implementation_status"], "observed")
            self.assertEqual(entries[item_id]["test_status"], "verified")
            self.assertTrue((ROOT / entries[item_id]["evidence"]).is_file())

    def test_every_verified_entry_has_auditable_evidence(self):
        verified = [row for row in self.catalog["entries"] if row["test_status"] == "verified"]
        self.assertTrue(verified)
        for row in verified:
            self.assertEqual(row["implementation_status"], "observed", row["id"])
            self.assertTrue(row.get("evidence"), row["id"])
            self.assertTrue((ROOT / row["evidence"]).is_file(), row["id"])

    def test_smoke_report_lists_every_finding_it_supports(self):
        expected = {row["id"] for row in self.catalog["entries"] if row.get("evidence") == "docs/smoke-findings.md"}
        report = (ROOT / "docs" / "smoke-findings.md").read_text(encoding="utf-8")
        documented = set()
        in_findings_table = False
        for line in report.splitlines():
            if line.startswith("| IDs"):
                in_findings_table = True
                continue
            if in_findings_table and not line.startswith("|"):
                break
            if not in_findings_table or line.startswith("|---"):
                continue
            values = line.split("|")[1].strip()
            documented.update(int(value.strip()) for value in values.split(","))
        self.assertEqual(documented, expected)

    def test_checked_in_checklist_matches_the_catalog(self):
        expected = render(self.catalog)
        actual = (ROOT / "vulndb" / "checklist.md").read_text(encoding="utf-8")
        self.assertEqual(actual, expected)

    def test_source_map_and_catalog_annotations_match_source(self):
        source_refs = collect_source_refs()
        expected_ids = set(source_refs)
        mapped = {
            row["id"]: row
            for row in self.catalog["entries"]
            if row.get("implementation_evidence") == "docs/implementation-map.md"
        }
        self.assertEqual(set(mapped), expected_ids)
        self.assertTrue(all(row["implementation_status"] == "observed" for row in mapped.values()))
        self.assertEqual(
            (ROOT / "docs" / "implementation-map.md").read_text(encoding="utf-8"),
            render_implementation_map(self.catalog, source_refs),
        )

    def test_source_observations_do_not_change_runtime_test_status(self):
        mapped = [
            row for row in self.catalog["entries"]
            if row.get("implementation_evidence") == "docs/implementation-map.md"
        ]
        self.assertTrue(mapped)
        self.assertTrue(all(row["test_status"] in {"not_tested", "verified"} for row in mapped))
        self.assertTrue(any(row["test_status"] == "not_tested" for row in mapped))

    def test_source_annotation_ids_match_the_catalog_topics(self):
        source_ids = set(collect_source_refs())
        self.assertTrue({72, 74, 75, 77, 480, 643, 648}.issubset(source_ids))
        self.assertTrue({40, 42, 227, 375}.isdisjoint(source_ids))

    def test_readme_contains_the_complete_inventory(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        start = readme.index(INVENTORY_START)
        end = readme.index(INVENTORY_END)
        section = readme[start:end]
        ids = []
        for line in section.splitlines():
            if not line.startswith("| "):
                continue
            first = line.split("|")[1].strip()
            if first.isdigit():
                ids.append(int(first))
        self.assertEqual(len(ids), 275 + 726)
        self.assertEqual(ids, list(range(1, 276)) + list(range(1, 727)))
        for row in self.catalog["components"][:5] + self.catalog["entries"][:5]:
            self.assertIn(row["name"].replace("|", "\\|"), section)

    def test_readme_preserves_every_moved_annotation(self):
        source_data = json.loads((ROOT / "vulndb" / "source-annotations.json").read_text(encoding="utf-8"))
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        start = readme.index(ANNOTATIONS_START)
        end = readme.index(ANNOTATIONS_END)
        section = readme[start:end]
        self.assertIn(f"**{len(source_data['annotations'])}** notes", section)
        for item in source_data["annotations"]:
            note = item["note"].replace("|", "\\|")
            self.assertIn(note, section)

    def test_readme_matches_the_generator(self):
        source_data = json.loads((ROOT / "vulndb" / "source-annotations.json").read_text(encoding="utf-8"))
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertEqual(readme, render_readme(readme, self.catalog, source_data))

    def test_source_tree_has_no_vulnerability_hints(self):
        import re

        hint = re.compile(
            r"\bVULN\b|vuln\s*#|#\s*vuln\b|(?i:intentionally|intentional|insecure|no auth)",
        )
        candidates = []
        for root in ("backend", "frontend", "services", "nginx"):
            candidates.extend((ROOT / root).rglob("*"))
        candidates.append(ROOT / "docker-compose.yml")
        offenders = []
        for path in candidates:
            if not path.is_file():
                continue
            if path.suffix not in {".py", ".js", ".ejs", ".yml", ".yaml", ".conf"} and not path.name.startswith("Dockerfile"):
                continue
            if {"node_modules", "__pycache__"} & set(path.parts):
                continue
            for number, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
                if hint.search(line):
                    offenders.append(f"{path.relative_to(ROOT).as_posix()}:{number}")
        self.assertEqual(offenders, [])

    def test_source_map_json_is_the_only_implementation_source(self):
        source_data = json.loads((ROOT / "vulndb" / "source-annotations.json").read_text(encoding="utf-8"))
        self.assertTrue(source_data["annotations"])
        self.assertTrue(all(item["path"] and item["symbol"] and item["note"] for item in source_data["annotations"]))
        self.assertTrue(all(isinstance(key, str) for key in source_data["ids"]))

    def test_checklist_ui_displays_verified_state_and_evidence(self):
        page = (ROOT / "vulndb" / "index.html").read_text(encoding="utf-8")
        self.assertIn("verified: 'Đã xác minh'", page)
        self.assertIn("Mã nguồn: ${row.implementation_evidence}", page)
        self.assertIn("Bằng chứng kiểm thử/audit: ${row.evidence}", page)
        self.assertIn("components.map(row => ({ ...row, record_type: 'component' }))", page)
        self.assertIn("node.textContent = safe(value)", page)


if __name__ == "__main__":
    unittest.main()
