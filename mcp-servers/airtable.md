# Airtable MCP Server

Query, create, update, and manage [Airtable](https://airtable.com/) bases, tables, records, and views from OpenCode.

**Package:** [`@rashidazarang/airtable-mcp`](https://www.npmjs.com/package/@rashidazarang/airtable-mcp)

## Prerequisites

- [Node.js](https://nodejs.org/) (v18+)
- An Airtable account with API access
- An Airtable Personal Access Token (PAT)

## Generating an Airtable Personal Access Token

1. Go to [airtable.com/create/tokens](https://airtable.com/create/tokens)
2. Click **Create new token**
3. Give it a name and select the scopes you need:
   - `data.records:read` / `data.records:write` -- Read and write records
   - `data.recordComments:read` / `data.recordComments:write` -- Comments
   - `schema.bases:read` / `schema.bases:write` -- Schema operations
   - `webhook:manage` -- Webhook management
4. Select which bases to grant access to (or all bases)
5. Copy the token (starts with `pat...`)

## Installation

Install the package globally or use npx. For a patched/local version:

```bash
git clone https://github.com/rashidazarang/airtable-mcp.git ~/sw_projects/airtable-mcp
cd ~/sw_projects/airtable-mcp
npm install
```

## Configuration

### Option A: Using npx (simplest)

```json
{
  "mcp": {
    "airtable": {
      "type": "local",
      "command": [
        "npx",
        "@rashidazarang/airtable-mcp"
      ],
      "environment": {
        "AIRTABLE_TOKEN": "patXXXXXXXXXXXXXX.XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
      },
      "enabled": true
    }
  }
}
```

### Option B: Using a local clone

```json
{
  "mcp": {
    "airtable": {
      "type": "local",
      "command": [
        "node",
        "/path/to/airtable-mcp/node_modules/@rashidazarang/airtable-mcp/bin/airtable-mcp.js"
      ],
      "environment": {
        "AIRTABLE_TOKEN": "patXXXXXXXXXXXXXX.XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
      },
      "enabled": true
    }
  }
}
```

Replace `AIRTABLE_TOKEN` with your Personal Access Token.

## Available Tools

### Bases & Schema
- `list_bases` -- List all accessible bases
- `get_base_schema` / `list_tables` -- View base structure
- `describe` -- Describe base or table schema in detail
- `create_base` / `create_table` / `create_field` -- Schema creation

### Records
- `query` -- Query records with filtering (formulas), sorting, pagination
- `search_records` -- Text search across a field
- `list_records` -- List records with field selection
- `get_record` -- Get a single record by ID
- `create` / `update` / `upsert` -- Record mutations (with dry-run support)
- `batch_create_records` / `batch_update_records` / `batch_delete_records` -- Batch operations (up to 10 at a time)

### Views & Comments
- `get_table_views` / `get_view_metadata` -- View management
- `list_comments` / `create_comment` / `update_comment` -- Record comments

### Webhooks
- `list_webhooks` / `create_webhook` / `delete_webhook` -- Webhook management

## Verification

After restarting OpenCode:

```
List my Airtable bases
```

```
Show me the tables in my Feature Interlock base
```
