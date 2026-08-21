from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SERVER_PATH = PLUGIN_ROOT / "server" / "uspto_mcp_server.py"
SPEC = importlib.util.spec_from_file_location("uspto_mcp_server", SERVER_PATH)
assert SPEC and SPEC.loader
server = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(server)


class ProtocolTests(unittest.TestCase):
    def test_self_test_runs_without_api_key(self) -> None:
        env = os.environ.copy()
        env.pop("USPTO_ODP_API_KEY", None)
        result = subprocess.run(
            [sys.executable, str(SERVER_PATH), "--self-test"],
            check=True,
            capture_output=True,
            text=True,
            env=env,
        )
        payload = json.loads(result.stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(8, len(payload["tools"]))

    def test_initialize_negotiates_supported_version(self) -> None:
        response = server.handle(
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {"protocolVersion": "2025-03-26"},
            }
        )
        self.assertEqual("2025-03-26", response["result"]["protocolVersion"])

    def test_ping(self) -> None:
        response = server.handle({"jsonrpc": "2.0", "id": 2, "method": "ping"})
        self.assertEqual({}, response["result"])

    def test_missing_key_is_safe_tool_error(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            response = server.handle(
                {
                    "jsonrpc": "2.0",
                    "id": 3,
                    "method": "tools/call",
                    "params": {
                        "name": "uspto_search_applications",
                        "arguments": {"query": "applicationMetaData.patentNumber:10049598"},
                    },
                }
            )
        self.assertTrue(response["result"]["isError"])
        message = response["result"]["content"][0]["text"]
        self.assertIn("USPTO_ODP_API_KEY is not set", message)


class ToolValidationTests(unittest.TestCase):
    def test_search_parameters_are_forwarded(self) -> None:
        with patch.object(server, "_get", return_value={"ok": True}) as get:
            result = server.call_tool(
                "uspto_search_applications",
                {
                    "query": "  applicationMetaData.patentNumber:10049598  ",
                    "offset": 2,
                    "limit": 5,
                    "sort": "applicationMetaData.filingDate:desc",
                    "fields": ["applicationMetaData", "inventors"],
                },
            )
        self.assertEqual({"ok": True}, result)
        get.assert_called_once_with(
            "/api/v1/patent/applications/search",
            {
                "q": "applicationMetaData.patentNumber:10049598",
                "offset": 2,
                "limit": 5,
                "sort": "applicationMetaData.filingDate:desc",
                "fields": "applicationMetaData,inventors",
            },
        )

    def test_rejects_invalid_limits(self) -> None:
        for value in (0, 101, True, "10"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    server.call_tool("uspto_search_applications", {"query": "x", "limit": value})

    def test_normalizes_application_number(self) -> None:
        with patch.object(server, "_get", return_value={}) as get:
            server.call_tool(
                "uspto_get_application_documents",
                {"application_number": "16/312,820"},
            )
        get.assert_called_once_with("/api/v1/patent/applications/16312820/documents")

    def test_rejects_unknown_tool(self) -> None:
        with self.assertRaisesRegex(ValueError, "Unknown tool"):
            server.call_tool("delete_application", {})


if __name__ == "__main__":
    unittest.main()
