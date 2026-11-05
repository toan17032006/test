import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.render_checklist import render


class CatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = json.loads((ROOT / "vulndb" / "catalog.json").read_text(encoding="utf-8"))

    def test_component_ids_and_count_are_complete(self):
        components = self.catalog["components"]
        self.assertEqual(len(components), 275)
        self.assertEqual([row["id"] for row in components], list(range(1, 276)))
        self.assertTrue(all(row["category"] and row["name"] for row in components))
        self.assertTrue(all(row["implementation_status"] == "unverified" for row in components))
        self.assertTrue(all(row["test_status"] == "not_tested" for row in components))

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

    def test_checked_in_checklist_matches_the_catalog(self):
        expected = render(self.catalog)
        actual = (ROOT / "vulndb" / "checklist.md").read_text(encoding="utf-8")
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
