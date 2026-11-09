import re
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]

INTERNAL_SERVICES = (
    "api",
    "graphql",
    "postgres",
    "mysql",
    "mongodb",
    "redis",
    "elasticsearch",
    "neo4j",
    "influxdb",
    "mailhog",
)


class ComposeSafetyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.compose_text = (ROOT / "docker-compose.yml").read_text(encoding="utf-8")
        cls.compose = yaml.safe_load(cls.compose_text)
        cls.services = cls.compose["services"]

    def published_ports(self, service):
        return [str(entry) for entry in self.services[service].get("ports", [])]

    @staticmethod
    def host_port(spec):
        return int(spec.rsplit(":", 1)[0].split(":")[-1])

    def test_every_published_host_port_is_above_9000(self):
        for service in self.services:
            for spec in self.published_ports(service):
                self.assertGreater(
                    self.host_port(spec),
                    9000,
                    f"{service} publishes {spec}, which is not above port 9000",
                )

    def test_storefront_and_nginx_are_reachable_from_other_hosts(self):
        frontend_ports = self.published_ports("frontend")
        nginx_ports = self.published_ports("nginx")
        self.assertIn("13000:3000", frontend_ports)
        self.assertIn("9080:80", nginx_ports)
        for spec in frontend_ports + nginx_ports:
            self.assertFalse(
                spec.startswith("127.0.0.1:"),
                f"External entry point {spec} is bound to loopback only",
            )

    def test_internal_services_stay_on_loopback(self):
        for service in INTERNAL_SERVICES:
            for spec in self.published_ports(service):
                self.assertTrue(
                    spec.startswith("127.0.0.1:"),
                    f"{service} publishes {spec} on a non-loopback interface",
                )

    def test_frontend_listens_on_all_interfaces_inside_the_container(self):
        environment = self.services["frontend"]["environment"]
        self.assertEqual(environment.get("HOST"), "0.0.0.0")
        self.assertEqual(environment.get("API_URL"), "http://api:8000")

    def test_lab_has_no_host_docker_socket_or_privileged_container(self):
        self.assertNotIn("/var/run/docker.sock", self.compose_text)
        self.assertIsNone(re.search(r"(?m)^\s*privileged:\s*true\b", self.compose_text))

    def test_default_network_blocks_outbound_egress(self):
        self.assertRegex(
            self.compose_text,
            r"(?m)^networks:\s*\n\s+default:\s*\n\s+internal:\s+true\b",
        )

    def test_real_git_metadata_is_not_mounted_into_the_web_server(self):
        self.assertNotRegex(self.compose_text, r"(?m)^\s*-\s+\.\/.git:")


if __name__ == "__main__":
    unittest.main()
