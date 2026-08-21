# Setup

## Credential

Create or sign in to a USPTO.gov account, satisfy the current ODP account requirements, and request a key at:

`https://data.uspto.gov/apis/getting-started`

Set the key in your local environment. Do not put the literal key in the MCP config or type it into a command that will be retained in shell history.

macOS with zsh for the current terminal:

```zsh
read -s "USPTO_ODP_API_KEY?USPTO ODP API key: "
export USPTO_ODP_API_KEY
printf '\n'
```

With bash on Linux, use:

```bash
read -rsp "USPTO ODP API key: " USPTO_ODP_API_KEY
export USPTO_ODP_API_KEY
printf '\n'
```

For persistent use, prefer the desktop application's secure environment-variable or secret field, or an operating-system credential manager. Do not place a literal key in a repository, project `.env` file, synchronized shell profile, or prompt. On macOS, a GUI-launched desktop app may not inherit terminal variables; use the app's secure environment-variable field if available.

## Codex plugin installation

The plugin already includes its MCP configuration. Install it from the public marketplace repository:

```bash
codex plugin marketplace add https://github.com/mihirkavi/uspto-patent-research-plugin
codex plugin add uspto-patent-research@patent-research
```

Restart Codex and open a new task so the installed skill and MCP tools are loaded. Verify the plugin with `codex plugin list` and look for `uspto_research` in `/mcp`.

For a source checkout, run `python3 plugins/uspto-patent-research/server/uspto_mcp_server.py --self-test`. This is an offline protocol test; a real search additionally requires the API key and network access.

## Compatibility

The bundled server requires Python 3.10 or newer and has no third-party Python dependencies. It is a local STDIO server; it does not make the user's API key available to chat or store it on disk.
