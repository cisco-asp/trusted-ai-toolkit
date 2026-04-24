# Obsidian MCP Server

Read, write, search, and manage notes in an [Obsidian](https://obsidian.md/) vault directly from OpenCode.

**Package:** [`@mauricio.wolff/mcp-obsidian`](https://www.npmjs.com/package/@mauricio.wolff/mcp-obsidian)

## What is Obsidian?

[Obsidian](https://obsidian.md/) is a free, cross-platform knowledge management application that stores notes as plain Markdown files in a local folder called a "vault." Unlike cloud-based note apps, your data stays entirely on your filesystem -- there is no proprietary format or vendor lock-in. Obsidian supports bidirectional linking between notes, creating a personal knowledge graph that makes it easy to connect ideas across topics. It also has a rich plugin ecosystem, tagging, YAML frontmatter for metadata, and a graph view for visualizing relationships between notes.

For SEs, Obsidian is useful for organizing customer notes, design docs, meeting minutes, runbooks, and technical reference material -- all in Markdown that works well with version control and AI tooling. With this MCP server, OpenCode can read, search, and update your vault directly during a session.

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
