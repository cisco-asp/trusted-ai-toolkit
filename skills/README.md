# Skills

Reusable agent skills bundled with the Trusted AI Toolkit. Skills extend an
OpenCode agent with specialized knowledge, workflows, and helper scripts that
load automatically when the agent recognizes a matching task.

## Quick install (recommended)

The easiest way to install skills from this repo is to ask OpenCode to do it
for you with a natural-language prompt. OpenCode will use the bundled
`find-skills` workflow to run the underlying `npx skills add` command and
register everything in `~/.agents/skills/`.

Examples you can paste straight into an OpenCode prompt:

```
Install the cisco-brand, deck, and pptx skills from
https://github.com/cisco-asp/trusted-ai-toolkit
```

```
Install all Cisco skills from cisco-asp/trusted-ai-toolkit
```

```
Add the crd-builder skill from the trusted-ai-toolkit repo
```

OpenCode resolves these requests to commands of the form:

```
npx skills add cisco-asp/trusted-ai-toolkit@<skill-name> -g -y
```

If you'd rather run it yourself, use the same command directly in a terminal.

## Available skills

| Skill | Purpose | Depends on / Pairs with |
|---|---|---|
| [`cisco-brand`](cisco-brand/) | Cisco brand guidelines (colors, typography, layout, dark/light themes) for any Cisco-branded output. | `pptx` (uses its bundled `.potx` templates) |
| [`cisco-config-lookup`](cisco-config-lookup/) | Search cisco.com configuration guides and command references for IOS-XR platforms (Cisco 8000, ASR 9000, NCS 5xx, XRd, etc.). | — |
| [`crd-builder`](crd-builder/) | Generate a Customer Requirements Document (CRD) from the bundled Cisco CRD `template.docx`. | — |
| [`deck`](deck/) | Build structured Cisco-branded presentation decks from outlines, notes, or raw content. Diagram-and-chart oriented, not bullet-heavy. | **Requires** `cisco-brand` and `pptx` |
| [`find-skills`](find-skills/) | Helps users discover and install other skills from the open agent skills ecosystem. | — |
| [`playwright-cli`](playwright-cli/) | Drive a browser via `playwright-cli` for testing, form-filling, screenshots, and data extraction. | — |
| [`pptx`](pptx/) | Create, edit, and analyze PowerPoint files. Includes Cisco `.potx` templates, OOXML editing scripts, HTML→PPTX conversion, and thumbnail generation. | Pairs with `cisco-brand` for branded output |

## Skill groups & dependencies

Some skills work standalone; others are part of a set. Install whole groups
together for the best experience.

### Cisco presentation bundle (install all three)

`cisco-brand`, `pptx`, and `deck` are designed to work together. The `deck`
skill explicitly loads `cisco-brand` for color/typography rules and uses the
official Cisco `.potx` templates that ship with the `pptx` skill. Installing
`deck` alone will produce broken output if the other two are missing.

```
Install the cisco-brand, pptx, and deck skills from cisco-asp/trusted-ai-toolkit
```

### Standalone skills

These have no inter-skill dependencies and can be installed individually:

- `cisco-config-lookup`
- `crd-builder`
- `find-skills`
- `playwright-cli`

## Verifying installation

After installation, confirm the skills are linked into your agent skills
directory:

```
ls ~/.agents/skills/
```

You should see the installed skill names (or symlinks) listed. Restart
OpenCode if it was running during installation so the new skills register.

## Updating

To update all installed skills:

```
npx skills update
```

Or ask OpenCode: *"Update all my installed skills."*
