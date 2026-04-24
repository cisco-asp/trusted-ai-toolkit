# Splunk MCP Server

Query Splunk from OpenCode using SPL, browse indexes, inspect metadata, and leverage the Splunk AI Assistant for natural language query generation.

**Connection method:** `mcp-remote` proxy to Splunk's built-in MCP endpoint

## Prerequisites

- [Node.js](https://nodejs.org/) (v18+)
- A Splunk Enterprise instance with the MCP service enabled (Splunk 9.4+)
- A Splunk authentication token

## Generating a Splunk Auth Token

1. Log in to your Splunk instance
2. Navigate to **Settings > Tokens** (or **Settings > Users > your-user > Tokens**)
3. Click **New Token**, set an expiration, and copy the token value

## Configuration

Add the following to your `~/.config/opencode/opencode.json`:

```json
{
  "mcp": {
    "splunk": {
      "type": "local",
      "command": [
        "npx",
        "mcp-remote",
        "https://YOUR_SPLUNK_HOST:8089/services/mcp",
        "--header",
        "Authorization: Bearer YOUR_SPLUNK_TOKEN"
      ],
      "environment": {
        "NODE_TLS_REJECT_UNAUTHORIZED": "0"
      },
      "enabled": true
    }
  }
}
```

Replace:
- `YOUR_SPLUNK_HOST` with your Splunk server hostname
- `YOUR_SPLUNK_TOKEN` with the bearer token from the step above

> **Note:** `NODE_TLS_REJECT_UNAUTHORIZED=0` disables TLS certificate verification. This is common for lab/internal Splunk instances with self-signed certs. Remove it if your Splunk instance has a valid certificate.

## Available Tools

- `splunk_run_query` -- Execute SPL queries with time range controls
- `splunk_get_indexes` / `splunk_get_index_info` -- Browse available indexes
- `splunk_get_metadata` -- List hosts, sources, and sourcetypes
- `splunk_get_user_list` / `splunk_get_user_info` -- User management info
- `splunk_get_knowledge_objects` -- Saved searches, alerts, macros, data models, etc.
- `splunk_get_kv_store_collections` -- KV Store statistics
- `saia_generate_spl` -- Natural language to SPL conversion (AI Assistant)
- `saia_explain_spl` -- Explain SPL queries in plain English
- `saia_optimize_spl` -- Optimize SPL query performance

## Verification

After restarting OpenCode:

```
What indexes are available in Splunk?
```

```
Search Splunk for errors in the last 24 hours
```
