from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
PLUGIN_ROOT = REPO_ROOT / "plugins" / "uspto-patent-research"


class PackagingTests(unittest.TestCase):
    def test_marketplace_points_to_plugin(self) -> None:
        marketplace = json.loads(
            (REPO_ROOT / ".agents" / "plugins" / "marketplace.json").read_text()
        )
        entry = marketplace["plugins"][0]
        self.assertEqual("patent-research", marketplace["name"])
        self.assertEqual("uspto-patent-research", entry["name"])
        self.assertEqual("./plugins/uspto-patent-research", entry["source"]["path"])
        self.assertTrue(PLUGIN_ROOT.is_dir())

    def test_manifest_paths_exist(self) -> None:
        manifest = json.loads(
            (PLUGIN_ROOT / ".codex-plugin" / "plugin.json").read_text()
        )
        self.assertEqual(PLUGIN_ROOT.name, manifest["name"])
        self.assertEqual("1.0.0", manifest["version"])
        for key in ("skills", "mcpServers"):
            path = PLUGIN_ROOT / manifest[key].removeprefix("./")
            self.assertTrue(path.exists(), f"missing manifest path: {path}")
        for key in ("composerIcon", "logo"):
            path = PLUGIN_ROOT / manifest["interface"][key].removeprefix("./")
            self.assertTrue(path.is_file(), f"missing interface asset: {path}")

    def test_mcp_server_path_exists(self) -> None:
        config = json.loads((PLUGIN_ROOT / ".mcp.json").read_text())
        server = config["mcpServers"]["uspto_research"]
        self.assertEqual("python3", server["command"])
        script = PLUGIN_ROOT / server["args"][0].removeprefix("./")
        self.assertTrue(script.is_file())
        self.assertIn("USPTO_ODP_API_KEY", server["env_vars"])

    def test_public_files_contain_no_placeholders(self) -> None:
        for path in REPO_ROOT.rglob("*"):
            if (
                path.is_file()
                and ".git" not in path.parts
                and "tests" not in path.parts
                and "__pycache__" not in path.parts
            ):
                try:
                    text = path.read_text()
                except UnicodeDecodeError:
                    continue
                self.assertNotIn("[TODO:", text, str(path))
                self.assertNotIn("/root/.codex/skills/remote-skills", text, str(path))


if __name__ == "__main__":
    unittest.main()
