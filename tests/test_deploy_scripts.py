import shutil
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


class DeployScriptTests(unittest.TestCase):
    def read(self, name):
        path = SCRIPTS / name
        self.assertTrue(path.is_file(), f"missing {name}")
        return path.read_text(encoding="utf-8")

    def test_all_launchers_exist_for_powershell_and_bash(self):
        for name in (
            "docker-up.ps1",
            "docker-up.sh",
            "dev-up.ps1",
            "dev-up.sh",
            "start-app.ps1",
            "start-app.sh",
        ):
            self.assertTrue((SCRIPTS / name).is_file(), f"missing scripts/{name}")

    def test_docker_launchers_build_images_and_start_frontend_and_backend(self):
        for name in ("docker-up.ps1", "docker-up.sh"):
            body = self.read(name)
            self.assertIn("docker compose", body, name)
            self.assertIn("build", body, name)
            self.assertIn("up -d", body, name)
            self.assertIn("18000", body, name)
            self.assertIn("13000", body, name)

    def test_native_launchers_publish_the_same_external_ports(self):
        for name in ("dev-up.ps1", "dev-up.sh"):
            body = self.read(name)
            self.assertIn("18000", body, name)
            self.assertIn("13000", body, name)
            self.assertIn("0.0.0.0", body, name)
            self.assertIn("API_URL", body, name)

    def test_one_command_entry_point_supports_docker_local_and_stop(self):
        powershell = self.read("start-app.ps1")
        self.assertIn("docker-up.ps1", powershell)
        self.assertIn("dev-up.ps1", powershell)
        self.assertIn("$Stop", powershell)
        self.assertIn("$Local", powershell)

        bash = self.read("start-app.sh")
        self.assertIn("docker-up.sh", bash)
        self.assertIn("dev-up.sh", bash)
        self.assertIn("--stop", bash)
        self.assertIn("--local", bash)

    def test_bash_launchers_are_syntactically_valid(self):
        bash = shutil.which("bash")
        if not bash:
            self.skipTest("bash is not available")
        for name in ("docker-up.sh", "dev-up.sh", "start-app.sh"):
            result = subprocess.run(
                [bash, "-n", str(SCRIPTS / name)],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_readme_reports_the_deployment(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for token in (
            "scripts/start-app.ps1",
            "scripts/start-app.sh",
            "scripts/docker-up.sh",
            "scripts/dev-up.sh",
            "13000",
            "18000",
            "9080",
        ):
            self.assertIn(token, readme, token)
        self.assertIn("trusted", readme.lower())


if __name__ == "__main__":
    unittest.main()
