import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ComposeSafetyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.compose = (ROOT / "docker-compose.yml").read_text(encoding="utf-8")

    def test_published_ports_are_bound_to_loopback(self):
        port_lines = [line.strip() for line in self.compose.splitlines() if re.match(r'^\s*-\s+"\d+:\d+"', line)]
        self.assertEqual(port_lines, [], "A published service port is bound to every host interface")
        published = [line.strip() for line in self.compose.splitlines() if re.match(r'^\s*-\s+"127\.0\.0\.1:\d+:\d+"', line)]
        self.assertGreater(len(published), 0, "Expected local-only published ports")

    def test_lab_has_no_host_docker_socket_or_privileged_container(self):
        self.assertNotIn("/var/run/docker.sock", self.compose)
        self.assertIsNone(re.search(r"(?m)^\s*privileged:\s*true\b", self.compose))

    def test_default_network_blocks_outbound_egress(self):
        self.assertRegex(self.compose, r"(?m)^networks:\s*\n\s+default:\s*\n\s+internal:\s+true\b")

    def test_real_git_metadata_is_not_mounted_into_the_web_server(self):
        self.assertNotRegex(self.compose, r"(?m)^\s*-\s+\.\/.git:")


if __name__ == "__main__":
    unittest.main()
