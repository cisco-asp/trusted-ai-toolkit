# Context7 MCP Server

Pull up-to-date, version-specific library documentation and code examples from [Context7](https://context7.com) directly into your OpenCode session. Eliminates hallucinated APIs and outdated examples that LLMs produce when relying on stale training data.

**Repo:** [upstash/context7](https://github.com/upstash/context7)
**Server URL:** `https://mcp.context7.com/mcp`
**Package (CLI):** [`ctx7`](https://www.npmjs.com/package/ctx7)
**Package (MCP server):** [`@upstash/context7-mcp`](https://www.npmjs.com/package/@upstash/context7-mcp)

## What is Context7?

Context7 indexes documentation and source examples for thousands of libraries (React, Next.js, Prisma, Supabase, Tailwind, Cloudflare Workers, MongoDB, etc.) and serves them on demand. Instead of letting the LLM guess at an API based on year-old training data, it fetches the actual current docs for the specific version you care about and injects them into the prompt.

For Cisco SEs, this is most useful when:

- Generating code that uses a fast-moving SDK or framework
- Verifying the correct CLI/API syntax for a tool before recommending it to a customer
- Migrating between major versions of a library
- Researching unfamiliar libraries during a customer engagement

## Prerequisites

- [Node.js](https://nodejs.org/) (v18+)
- A Context7 API key (free tier is fine — generate one at [context7.com/dashboard](https://context7.com/dashboard))

> **Why an API key?** Unauthenticated requests are heavily rate-limited. The free key raises the cap significantly and is required for any real workflow.

## Installation

Two options. Pick one.

### Option A: One-command installer (recommended)

Context7 ships its own installer that handles OAuth, generates an API key, and writes the right config into your OpenCode setup automatically:

```bash
npx ctx7 setup --opencode
```

When prompted, choose **MCP mode** (vs. CLI + Skills mode). Restart OpenCode after it finishes.

To remove the integration later:

```bash
npx ctx7 remove
```

### Option B: Manual configuration

If you prefer to wire it up by hand, add the following to your `~/.config/opencode/opencode.json` (global) or project-level `opencode.json`:

```json
{
  "mcp": {
    "context7": {
      "type": "remote",
      "url": "https://mcp.context7.com/mcp",
      "headers": {
        "CONTEXT7_API_KEY": "ctx7_your_key_here"
      },
      "enabled": true
    }
  }
}
```

Replace `ctx7_your_key_here` with the API key from [context7.com/dashboard](https://context7.com/dashboard). Restart OpenCode.

## Available Tools

Once configured, OpenCode gains two MCP tools:

- `resolve-library-id` -- Resolves a plain library name (e.g. "Next.js") into a Context7 library ID (e.g. `/vercel/next.js`)
- `query-docs` -- Fetches docs for a given library ID and a question

You normally don't call these by name -- the agent invokes them automatically when it recognizes a library/framework question.

## Pairs well with the `context7-mcp` skill

The Trusted AI Toolkit ships a [`context7-mcp` skill](../skills/context7-mcp/) that teaches the agent **when** to reach for Context7 (basically: any time the user asks about a library, framework, SDK, API, or CLI tool — even well-known ones, since training data may be stale). Install both together for the best behavior:

```
Install the context7-mcp skill from cisco-asp/trusted-ai-toolkit
```

Without the skill, the agent will only call Context7 when the user explicitly says "use context7" in their prompt.

## Tips

- **Pin a version**: Mention the version in your prompt and Context7 will fetch docs for that release: *"How do I configure middleware in Next.js 14?"*
- **Pin a library directly**: If you already know the library ID, include it: *"Implement basic auth with Supabase. use library /supabase/supabase"*
- **Trigger phrase**: Adding *"use context7"* to a prompt forces the agent to consult Context7 even without the skill installed.

## Verification

After restarting OpenCode, ask it something library-specific:

```
What's the recommended way to set up authentication in Next.js 15? use context7
```

The agent should call `resolve-library-id` followed by `query-docs` and return current Next.js 15 docs (not pre-2024 patterns).

## More information

- [Context7 website](https://context7.com)
- [Manual setup for other MCP clients](https://context7.com/docs/resources/all-clients)
- [Context7 GitHub repo](https://github.com/upstash/context7)
