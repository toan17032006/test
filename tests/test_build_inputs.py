import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class BuildInputTests(unittest.TestCase):
    def test_compose_dockerfiles_and_file_binds_exist(self):
        compose = (ROOT / "docker-compose.yml").read_text(encoding="utf-8")
        contexts = {}
        current_context = None
        for line in compose.splitlines():
            context = re.match(r"\s*context:\s*\.\/([^\s]+)", line)
            if context:
                current_context = context.group(1)
            dockerfile = re.match(r"\s*dockerfile:\s*([^\s]+)", line)
            if dockerfile and current_context:
                contexts[current_context] = dockerfile.group(1)
                current_context = None
        self.assertGreater(len(contexts), 0)
        for context, dockerfile in contexts.items():
            self.assertTrue((ROOT / context / dockerfile).is_file(), f"missing {context}/{dockerfile}")

        for source in re.findall(r"(?m)^\s+-\s+\.?\.?/?\.?\/([^:\s]+):[^\s]+", compose):
            self.assertTrue((ROOT / source).exists(), f"missing Compose bind source {source}")

    def test_frontend_catalog_mount_matches_service_setting(self):
        compose = (ROOT / "docker-compose.yml").read_text(encoding="utf-8")
        self.assertIn("VULNDB_DIR: /vulndb", compose)
        self.assertIn("./vulndb:/vulndb:ro", compose)

    def test_docker_contexts_exclude_local_dependencies_and_secrets(self):
        for relative in ("frontend/.dockerignore", "backend/.dockerignore", "services/graphql/.dockerignore", "services/worker/.dockerignore"):
            ignore_file = ROOT / relative
            self.assertTrue(ignore_file.is_file(), relative)
            contents = ignore_file.read_text(encoding="utf-8")
            self.assertIn(".env", contents, relative)
        self.assertIn("node_modules", (ROOT / "frontend" / ".dockerignore").read_text(encoding="utf-8"))
        self.assertIn("node_modules", (ROOT / "services" / "graphql" / ".dockerignore").read_text(encoding="utf-8"))

    def test_ci_workflow_uses_read_only_repository_permissions(self):
        workflow = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
        self.assertIn("contents: read", workflow)
        self.assertIn("npm test", workflow)
        self.assertIn("python -m unittest discover -s tests -v", workflow)


if __name__ == "__main__":
    unittest.main()
