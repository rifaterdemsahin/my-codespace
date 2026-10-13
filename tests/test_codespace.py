#!/usr/bin/env python3
"""
Automated Test Suite for Local & Cloud Codespace
Validates devcontainer configuration, Docker container state, Antigravity CLI,
projects directory mounting, and HTTP workbench accessibility.
"""

import json
import os
import subprocess
import unittest
import urllib.request
import urllib.error

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEVCONTAINER_PATH = os.path.join(PROJECT_ROOT, ".devcontainer", "devcontainer.json")
CONTAINER_NAME = "my-codespace-local"
PORT = 8080
BASE_URL = f"http://localhost:{PORT}"


class TestDevContainerConfig(unittest.TestCase):
    """Validates the .devcontainer configuration schema and values."""

    def test_devcontainer_file_exists(self):
        self.assertTrue(os.path.isfile(DEVCONTAINER_PATH), "devcontainer.json must exist")

    def test_devcontainer_json_syntax(self):
        with open(DEVCONTAINER_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIsInstance(data, dict, "devcontainer.json must be a valid JSON object")
        self.assertIn("name", data)
        self.assertIn("image", data)
        self.assertIn("forwardPorts", data)
        self.assertIn(8080, data["forwardPorts"], "Port 8080 must be forwarded")
        self.assertIn("customizations", data)
        vscode_exts = data.get("customizations", {}).get("vscode", {}).get("extensions", [])
        self.assertIn("dbaeumer.vscode-eslint", vscode_exts)
        self.assertIn("esbenp.prettier-vscode", vscode_exts)


class TestDockerAndContainer(unittest.TestCase):
    """Validates Docker daemon, running container state, and mounts."""

    def test_docker_daemon_running(self):
        result = subprocess.run(
            ["sudo", "docker", "info"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        self.assertEqual(result.returncode, 0, f"Docker daemon must be reachable: {result.stderr}")

    def test_container_is_running(self):
        result = subprocess.run(
            ["sudo", "docker", "inspect", "-f", "{{.State.Running}}", CONTAINER_NAME],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        self.assertEqual(result.returncode, 0, f"Container {CONTAINER_NAME} must exist")
        self.assertEqual(result.stdout.strip(), "true", f"Container {CONTAINER_NAME} must be in running state")

    def test_projects_volume_mounted(self):
        result = subprocess.run(
            ["sudo", "docker", "exec", CONTAINER_NAME, "test", "-d", "/home/coder/projects/my-codespace"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        self.assertEqual(result.returncode, 0, "~/projects must be mounted at /home/coder/projects")

    def test_antigravity_installed_and_functional(self):
        result = subprocess.run(
            ["sudo", "docker", "exec", "-u", "coder", CONTAINER_NAME, "agy", "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        self.assertEqual(result.returncode, 0, f"Antigravity CLI (agy) must run in container: {result.stderr}")
        self.assertTrue(len(result.stdout.strip()) > 0, "agy --version must return version output")


class TestHttpEndpoints(unittest.TestCase):
    """Validates HTTP endpoints and web workbench availability."""

    def test_root_redirects_to_projects_without_auth(self):
        class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
            def http_error_302(self, req, fp, code, msg, headers):
                return fp

        opener = urllib.request.build_opener(NoRedirectHandler)
        req = urllib.request.Request(f"{BASE_URL}/", headers={"User-Agent": "HealthCheckTest/1.0"})
        resp = opener.open(req, timeout=5)
        self.assertEqual(resp.status, 302, "Root URL should return HTTP 302 redirect")
        location = resp.headers.get("Location")
        self.assertTrue(
            location.endswith("?folder=~/projects") or location.endswith("?folder=/home/coder/projects"),
            f"Expected redirect directly to ~/projects, got: {location}"
        )

    def test_workbench_html_loads(self):
        req = urllib.request.Request(f"{BASE_URL}/?folder=/home/coder/projects", headers={"User-Agent": "HealthCheckTest/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            self.assertEqual(resp.status, 200, "Projects folder endpoint must return HTTP 200")
            content = resp.read().decode("utf-8")
            self.assertIn("vscode-workbench", content, "Response must contain VS Code web workbench configuration")


if __name__ == "__main__":
    unittest.main(verbosity=2)
