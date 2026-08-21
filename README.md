# USPTO Patent Research Plugin

A public, read-only Codex plugin for researching U.S. patent applications through the USPTO Open Data Portal (ODP). It combines eight MCP tools with a structured patent-research skill so Codex can search public application records, inspect prosecution history, and organize evidence without filing or changing anything at the USPTO.

> [!IMPORTANT]
> This is an independent research tool, not an official USPTO product and not legal advice. It does not determine patentability, infringement, validity, or freedom to operate. Have a registered patent practitioner review work before relying on it or filing.

## What it does

- Searches public Patent File Wrapper application records.
- Reads application metadata, continuity, foreign priority, transactions, document lists, and recorded assignments.
- Guides prior-art landscapes, claim-element matrices, disclosures, and draft specifications.
- Keeps the USPTO API key in the user's local environment.
- Uses only read-only HTTP `GET` requests and has no filing, payment, signing, or account-mutation tools.

## Requirements

- Codex with plugin support
- Python 3.10 or newer (no third-party Python packages)
- A USPTO.gov account with ODP access and an API key from the [USPTO getting-started page](https://data.uspto.gov/apis/getting-started)

## Install

Add this repository as a marketplace, then install the plugin:

```bash
codex plugin marketplace add mihirkavi/uspto-patent-research-plugin
codex plugin add uspto-patent-research@patent-research
```

Make the API key available as `USPTO_ODP_API_KEY` before starting Codex. On macOS or Linux, this hidden prompt avoids placing the literal key in shell history:

```bash
read -rsp "USPTO ODP API key: " USPTO_ODP_API_KEY
export USPTO_ODP_API_KEY
printf '\n'
```

Restart Codex, open a new task, and check `/mcp` for `uspto_research`. Try:

```text
Use $uspto-patent-research to search USPTO records for prior art related to adaptive meal nutrition estimation.
```

For persistent credentials, use a secure local environment or operating-system credential mechanism. Do not commit the key, place it in prompts, or add it directly to plugin files.

## Available tools

| Tool | Purpose |
| --- | --- |
| `uspto_search_applications` | Search application records with ODP query syntax |
| `uspto_get_application_record` | Read a complete public application record |
| `uspto_get_application_metadata` | Read bibliographic and status metadata |
| `uspto_get_application_continuity` | Read domestic continuity data |
| `uspto_get_application_transactions` | Read prosecution transaction history |
| `uspto_get_application_documents` | List public file-wrapper documents |
| `uspto_get_application_assignments` | Read recorded assignment data |
| `uspto_get_application_foreign_priority` | Read foreign-priority data |

## Verify a source checkout

The offline suite checks packaging, JSON-RPC behavior, tool schemas, input validation, error handling, and request construction without needing a credential:

```bash
python3 -m unittest discover -s plugins/uspto-patent-research/tests -v
python3 plugins/uspto-patent-research/server/uspto_mcp_server.py --self-test
```

A passing offline test proves the plugin and MCP protocol are wired correctly. It does not prove that a particular USPTO account/key currently has live ODP access. With `USPTO_ODP_API_KEY` set, verify live access with:

```bash
python3 plugins/uspto-patent-research/server/uspto_mcp_server.py \
  --search 'applicationMetaData.patentNumber:10049598' --limit 1
```

## Repository layout

```text
.agents/plugins/marketplace.json       Public Codex marketplace catalog
plugins/uspto-patent-research/
├── .codex-plugin/plugin.json          Plugin manifest
├── .mcp.json                          Local STDIO MCP registration
├── server/uspto_mcp_server.py         Dependency-free read-only server
├── skills/uspto-patent-research/      Research workflow and references
└── tests/                              Offline behavior and packaging tests
```

## Limitations

- ODP access requires a current USPTO account and API key; USPTO account requirements and rate limits can change.
- ODP metadata and file-wrapper records are not a complete prior-art search. Full-text patent sources, non-patent literature, citation networks, and professional judgment remain necessary.
- The plugin does not download document contents, search every patent authority, file applications, pay fees, or modify USPTO records.
- Local STDIO plugins run on the user's machine. Browser-only environments need a separately hosted, authenticated MCP service, which this repository does not provide.

See [PRIVACY.md](PRIVACY.md), [SECURITY.md](SECURITY.md), and [CONTRIBUTING.md](CONTRIBUTING.md) for public-use details.

## License

[MIT](LICENSE)
