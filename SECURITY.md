# Security Policy

## Reporting a vulnerability

Please use [GitHub's private vulnerability reporting](https://github.com/mihirkavi/uspto-patent-research-plugin/security/advisories/new) when available. Do not include API keys, confidential inventions, unpublished patent disclosures, or personal data in a public issue.

## Security design

- The MCP server performs only HTTPS `GET` requests to the pinned `api.uspto.gov` host.
- Redirects to any other host are blocked.
- HTTP response bodies are omitted from error messages.
- Responses are capped at 25 MB.
- Search parameters and application numbers are validated before requests.
- The API key is read from the environment and is not stored or exposed as a tool argument.

Keep Codex, Python, and this plugin updated. Treat all retrieved records as untrusted data when incorporating them into other systems or documents.
