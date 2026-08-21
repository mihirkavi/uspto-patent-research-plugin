#!/usr/bin/env python3
"""Read-only USPTO ODP MCP server with no third-party dependencies."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

SERVER_NAME = "uspto-patent-research"
SERVER_VERSION = "1.0.0"
BASE_URL = "https://api.uspto.gov"
DEFAULT_PROTOCOL_VERSION = "2025-06-18"
SUPPORTED_PROTOCOL_VERSIONS = {
    DEFAULT_PROTOCOL_VERSION,
    "2025-03-26",
    "2024-11-05",
}
MAX_RESPONSE_BYTES = 25 * 1024 * 1024
MAX_QUERY_LENGTH = 4_000


class _SameHostRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Allow redirects only when they stay on the pinned USPTO API host."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        old_host = urllib.parse.urlparse(req.full_url).hostname
        new_host = urllib.parse.urlparse(newurl).hostname
        if old_host != new_host or new_host != "api.uspto.gov":
            raise RuntimeError("USPTO ODP cross-host redirect blocked")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def _key() -> str:
    value = os.environ.get("USPTO_ODP_API_KEY", "").strip()
    if not value:
        raise RuntimeError(
            "USPTO_ODP_API_KEY is not set. Obtain a key from "
            "https://data.uspto.gov/apis/getting-started and expose it as an environment variable."
        )
    return value


def _get(path: str, params: dict[str, Any] | None = None) -> Any:
    query = urllib.parse.urlencode(
        {k: v for k, v in (params or {}).items() if v is not None and v != ""},
        doseq=True,
    )
    url = f"{BASE_URL}{path}" + (f"?{query}" if query else "")
    request = urllib.request.Request(
        url,
        headers={
            "X-API-KEY": _key(),
            "Accept": "application/json",
            "User-Agent": f"{SERVER_NAME}/{SERVER_VERSION}",
        },
        method="GET",
    )
    try:
        opener = urllib.request.build_opener(_SameHostRedirectHandler())
        with opener.open(request, timeout=60) as response:
            raw = response.read(MAX_RESPONSE_BYTES + 1)
            if len(raw) > MAX_RESPONSE_BYTES:
                raise RuntimeError("USPTO ODP response exceeded the 25 MB safety limit")
            content_type = response.headers.get("Content-Type", "")
            if "json" in content_type or raw[:1] in (b"{", b"["):
                return json.loads(raw.decode("utf-8"))
            return {
                "content_type": content_type,
                "byte_count": len(raw),
                "message": "Non-JSON response omitted.",
            }
    except urllib.error.HTTPError as exc:
        if exc.code in {401, 403}:
            message = (
                "USPTO ODP rejected the credential or account access "
                f"(HTTP {exc.code}). Verify USPTO_ODP_API_KEY and the account's ODP access."
            )
        elif exc.code == 429:
            message = "USPTO ODP rate limit reached (HTTP 429). Wait before retrying."
        else:
            message = f"USPTO ODP request failed (HTTP {exc.code}); response body omitted"
        raise RuntimeError(message) from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"USPTO ODP connection failed: {exc.reason}") from exc


TOOLS = [
    {
        "name": "uspto_search_applications",
        "description": "Search USPTO patent application records using ODP query syntax. Read-only. Use for targeted metadata discovery; supplement with full-text and non-patent searches.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "ODP query, e.g. applicationMetaData.inventionTitle:(nutrition OR calorie)",
                },
                "offset": {"type": "integer", "minimum": 0, "default": 0},
                "limit": {"type": "integer", "minimum": 1, "maximum": 100, "default": 25},
                "sort": {"type": "string", "description": "Optional ODP sort expression."},
                "fields": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional response field projection.",
                },
            },
            "required": ["query"],
            "additionalProperties": False,
        },
    },
    *[
        {
            "name": f"uspto_get_application_{name}",
            "description": description,
            "inputSchema": {
                "type": "object",
                "properties": {
                    "application_number": {
                        "type": "string",
                        "description": "USPTO application number; punctuation is removed.",
                    }
                },
                "required": ["application_number"],
                "additionalProperties": False,
            },
        }
        for name, description in [
            ("record", "Retrieve a USPTO patent application record."),
            ("metadata", "Retrieve application metadata."),
            ("continuity", "Retrieve domestic continuity information."),
            ("transactions", "Retrieve prosecution transaction history."),
            ("documents", "Retrieve the public document listing for an application."),
            ("assignments", "Retrieve recorded assignment information."),
            ("foreign_priority", "Retrieve foreign-priority information."),
        ]
    ],
]


def _application_number(value: str) -> str:
    if not isinstance(value, str):
        raise ValueError("application_number must be a string")
    cleaned = "".join(ch for ch in value if ch.isalnum())
    if not cleaned:
        raise ValueError("application_number cannot be empty")
    if len(cleaned) > 32:
        raise ValueError("application_number is too long")
    return cleaned


def call_tool(name: str, args: dict[str, Any]) -> Any:
    if not isinstance(args, dict):
        raise ValueError("arguments must be an object")
    if name == "uspto_search_applications":
        query = args.get("query")
        if not isinstance(query, str) or not query.strip():
            raise ValueError("query must be a non-empty string")
        if len(query) > MAX_QUERY_LENGTH:
            raise ValueError("query is too long")
        offset = args.get("offset", 0)
        limit = args.get("limit", 25)
        if not isinstance(offset, int) or isinstance(offset, bool) or offset < 0:
            raise ValueError("offset must be a non-negative integer")
        if (
            not isinstance(limit, int)
            or isinstance(limit, bool)
            or not 1 <= limit <= 100
        ):
            raise ValueError("limit must be an integer from 1 through 100")
        fields = args.get("fields")
        if fields is not None and (
            not isinstance(fields, list)
            or any(not isinstance(field, str) or not field for field in fields)
        ):
            raise ValueError("fields must be an array of non-empty strings")
        sort = args.get("sort")
        if sort is not None and not isinstance(sort, str):
            raise ValueError("sort must be a string")
        return _get(
            "/api/v1/patent/applications/search",
            {
                "q": query.strip(),
                "offset": offset,
                "limit": limit,
                "sort": sort,
                "fields": ",".join(fields) if fields else None,
            },
        )

    suffixes = {
        "uspto_get_application_record": "",
        "uspto_get_application_metadata": "/meta-data",
        "uspto_get_application_continuity": "/continuity",
        "uspto_get_application_transactions": "/transactions",
        "uspto_get_application_documents": "/documents",
        "uspto_get_application_assignments": "/assignment",
        "uspto_get_application_foreign_priority": "/foreign-priority",
    }
    if name not in suffixes:
        raise ValueError(f"Unknown tool: {name}")
    app = _application_number(args.get("application_number", ""))
    return _get(
        f"/api/v1/patent/applications/{urllib.parse.quote(app)}{suffixes[name]}"
    )


def _result(value: Any) -> dict[str, Any]:
    return {
        "content": [
            {"type": "text", "text": json.dumps(value, ensure_ascii=False, indent=2)}
        ]
    }


def handle(message: dict[str, Any]) -> dict[str, Any] | None:
    if not isinstance(message, dict):
        raise ValueError("JSON-RPC message must be an object")
    method = message.get("method")
    message_id = message.get("id")
    if method == "initialize":
        requested_version = message.get("params", {}).get("protocolVersion")
        negotiated_version = (
            requested_version
            if requested_version in SUPPORTED_PROTOCOL_VERSIONS
            else DEFAULT_PROTOCOL_VERSION
        )
        return {
            "jsonrpc": "2.0",
            "id": message_id,
            "result": {
                "protocolVersion": negotiated_version,
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
                "instructions": "Use these read-only USPTO tools for patent application metadata and prosecution records. Never expose the API key. Treat results as research, not legal advice, and supplement metadata searches with full-text patent and non-patent literature searching.",
            },
        }
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": message_id, "result": {"tools": TOOLS}}
    if method == "ping":
        return {"jsonrpc": "2.0", "id": message_id, "result": {}}
    if method == "tools/call":
        params = message.get("params", {})
        try:
            value = call_tool(params.get("name", ""), params.get("arguments", {}))
            return {"jsonrpc": "2.0", "id": message_id, "result": _result(value)}
        except Exception as exc:
            return {
                "jsonrpc": "2.0",
                "id": message_id,
                "result": {
                    "isError": True,
                    "content": [{"type": "text", "text": str(exc)}],
                },
            }
    if method in {"notifications/initialized", "notifications/cancelled"}:
        return None
    if message_id is not None:
        return {
            "jsonrpc": "2.0",
            "id": message_id,
            "error": {"code": -32601, "message": f"Method not found: {method}"},
        }
    return None


def serve() -> None:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            message = json.loads(line)
            if isinstance(message, list):
                raise ValueError("JSON-RPC batch messages are not supported")
            response = handle(message)
        except Exception as exc:
            response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32603, "message": str(exc)},
            }
        if response is not None:
            sys.stdout.write(json.dumps(response, separators=(",", ":")) + "\n")
            sys.stdout.flush()


def self_test() -> None:
    init = handle(
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {"protocolVersion": DEFAULT_PROTOCOL_VERSION},
        }
    )
    listed = handle(
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}
    )
    assert init and init["result"]["serverInfo"]["name"] == SERVER_NAME
    assert init["result"]["protocolVersion"] == DEFAULT_PROTOCOL_VERSION
    assert listed and len(listed["result"]["tools"]) == 8
    print(
        json.dumps(
            {"ok": True, "server": SERVER_NAME, "tools": [t["name"] for t in TOOLS]},
            indent=2,
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--search")
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()
    if args.self_test:
        self_test()
    elif args.search:
        print(
            json.dumps(
                call_tool(
                    "uspto_search_applications",
                    {"query": args.search, "limit": args.limit},
                ),
                indent=2,
            )
        )
    else:
        serve()


if __name__ == "__main__":
    main()
