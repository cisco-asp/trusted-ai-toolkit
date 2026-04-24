# MCP Servers

[Model Context Protocol (MCP)](https://modelcontextprotocol.io/) servers extend OpenCode with the ability to interact with external systems -- infrastructure platforms, data stores, documentation vaults, and more.

Each MCP server runs as a local process (or connects to a remote endpoint) and exposes tools that OpenCode can call during your session.

## Available Servers

| Server | Description | Guide |
|--------|-------------|-------|
| **Obsidian** | Read, write, and search Obsidian vault notes | [obsidian.md](obsidian.md) |
| **Splunk** | Run SPL queries, browse indexes, AI-assisted search | [splunk.md](splunk.md) |
| **NetBox** | Query DCIM/IPAM infrastructure data (devices, IPs, VLANs) | [netbox.md](netbox.md) |
| **Kubernetes** | Manage clusters -- pods, logs, exec, deployments, scaling | [kubernetes.md](kubernetes.md) |
| **Airtable** | Query and manage Airtable bases, tables, and records | [airtable.md](airtable.md) |

## How MCP Servers Work in OpenCode

MCP servers are configured in your `opencode.json` config file (either global at `~/.config/opencode/opencode.json` or per-project). Each entry specifies:

- **`type`** -- `"local"` (runs a command) or `"remote"` (connects to a URL)
- **`command`** -- The command to start the server (for local servers)
- **`environment`** -- Environment variables (API tokens, URLs, etc.)
- **`enabled`** -- Toggle the server on/off

Example structure:

```json
{
  "mcp": {
    "server-name": {
      "type": "local",
      "command": ["npx", "some-mcp-server@latest"],
      "environment": {
        "API_TOKEN": "your-token-here"
      },
      "enabled": true
    }
  }
}
```

After adding a server, restart OpenCode. The server's tools become available immediately -- no skill or plugin installation needed.

## Security Notes

- API tokens and credentials in `opencode.json` are stored in plaintext. Keep your global config file permissions restrictive (`chmod 600`).
- Servers that use `NODE_TLS_REJECT_UNAUTHORIZED=0` disable TLS certificate verification. This is acceptable for lab environments with self-signed certs but should not be used in production.
- Do not commit `opencode.json` files containing real tokens to version control.
