import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class FrontendViewTests(unittest.TestCase):
    def test_every_rendered_view_exists(self):
        source = (ROOT / "frontend" / "routes" / "index.js").read_text(encoding="utf-8")
        views = set(re.findall(r"res\.render\(['\"]([^'\"]+)", source))
        files = {path.stem for path in (ROOT / "frontend" / "views").glob("*.ejs")}
        self.assertEqual(views - files, set())

    def test_all_ejs_includes_resolve(self):
        views_dir = ROOT / "frontend" / "views"
        includes = set()
        for path in views_dir.rglob("*.ejs"):
            includes.update(re.findall(r"include\(['\"]([^'\"]+)", path.read_text(encoding="utf-8")))
        for include in includes:
            self.assertTrue((views_dir / f"{include}.ejs").exists(), include)

    def test_shared_assets_exist(self):
        self.assertTrue((ROOT / "frontend" / "public" / "css" / "style.css").is_file())
        self.assertTrue((ROOT / "frontend" / "public" / "js" / "app.js").is_file())

    def test_storefront_reads_backend_product_response_shapes(self):
        routes = (ROOT / "frontend" / "routes" / "index.js").read_text(encoding="utf-8")
        self.assertIn("Array.isArray(r.data.products)", routes)
        self.assertIn("product = r.data.product", routes)
        self.assertIn("Array.isArray(r.data.reviews)", routes)


if __name__ == "__main__":
    unittest.main()
