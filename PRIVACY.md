# Privacy

## Data handled

The plugin processes search queries and U.S. patent application numbers supplied through Codex. When a USPTO tool is used, the local MCP server sends the request to `https://api.uspto.gov` with the user's `USPTO_ODP_API_KEY` in the `X-API-KEY` header and returns the public response to Codex.

## Storage and logging

The plugin does not include analytics, telemetry, a database, or persistent request logging. It does not write the API key, tool arguments, or API responses to disk. Codex, the user's operating system, and the USPTO may handle data under their own policies.

## Credentials

The API key is read from the local `USPTO_ODP_API_KEY` environment variable at request time. It is never part of a tool schema or response. Users should not place credentials in prompts, source files, MCP configuration values, `.env` files committed to version control, or issue reports.

## Scope

The server exposes only read-only public-record requests. It cannot file applications, sign documents, pay fees, or modify USPTO data.

Questions or privacy reports can be opened through the repository's [GitHub issues](https://github.com/mihirkavi/uspto-patent-research-plugin/issues) without including confidential invention details or credentials.
