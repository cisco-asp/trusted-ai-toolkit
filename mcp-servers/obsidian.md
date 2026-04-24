# Obsidian MCP Server

Read, write, search, and manage notes in an [Obsidian](https://obsidian.md/) vault directly from OpenCode.

**Package:** [`@mauricio.wolff/mcp-obsidian`](https://www.npmjs.com/package/@mauricio.wolff/mcp-obsidian)

## Prerequisites

- [Node.js](https://nodejs.org/) (v18+)
- An Obsidian vault on your local filesystem

## Configuration

Add the following to your `~/.config/opencode/opencode.json` (global) or project-level `opencode.json`:

```json
{
  "mcp": {
    "obsidian": {
      "type": "local",
      "command": [
        "npx",
        "@mauricio.wolff/mcp-obsidian@latest",
        "/path/to/your/obsidian/vault"
      ],
      "enabled": true
    }
  }
}
```

Replace `/path/to/your/obsidian/vault` with the absolute path to your vault directory.

## Multiple Vaults

You can configure multiple Obsidian vaults by adding separate entries with different names:

```json
{
  "mcp": {
    "obsidian-personal": {
      "type": "local",
      "command": [
        "npx",
        "@mauricio.wolff/mcp-obsidian@latest",
        "/path/to/personal/vault"
      ],
      "enabled": true
    },
    "obsidian-work": {
      "type": "local",
      "command": [
        "npx",
        "@mauricio.wolff/mcp-obsidian@latest",
        "/path/to/work/vault"
      ],
      "enabled": true
    }
  }
}
```

## Available Tools

Once configured, OpenCode gains these capabilities:

- `read_note` / `read_multiple_notes` -- Read note content and frontmatter
- `write_note` -- Create or overwrite notes
- `patch_note` -- Partial string replacement within a note
- `search_notes` -- Full-text search across the vault
- `list_directory` -- Browse vault folder structure
- `move_note` / `delete_note` -- File management
- `manage_tags` -- Add, remove, or list tags
- `update_frontmatter` / `get_frontmatter` -- YAML frontmatter operations
- `get_vault_stats` -- Vault size, note count, recent files

## Verification

After restarting OpenCode, ask it to list your vault contents:

```
List the files in my Obsidian vault
```
