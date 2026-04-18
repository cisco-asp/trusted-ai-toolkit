# Getting Started with OpenCode and GitHub Copilot

Within Cisco, you must adhere to the policies regarding the sharing of data with specific model providers. As of the date of this writing, you can not use personal subscriptions with Cisco Confidential data (including customer data).

Cisco maintains enterprise solutions that are approved for highly confidential data. GitHub Copilot is such a solution. Through this agreement, Cisco and customer data is not used in training or reinforcement learning.

## Installation Process

### Step 1: Enable Access to GitHub Copilot

Request access here:
<https://appstore.cisco.com/details/github-copilot>

After successful registration, you will receive an email confirming you have access. Note that your login to GitHub Copilot is a different username and will use Cisco SSO authentication. Your username will be **yourcecid_cisco**.

### Step 2: Download and Install OpenCode

You have two options here due to the recent release of OpenCode's Desktop UI. Some are very comfortable working in the terminal while others may prefer a more app-like experience. These two are not exclusive -- the harness is independent of the UI so you can use either or both if you prefer.

#### Option A: OpenCode Terminal (CLI/TUI)

The terminal version runs directly in your shell. Install using any of the following methods:

```bash
# Install script (easiest)
curl -fsSL https://opencode.ai/install | bash

# Or via Homebrew (macOS/Linux)
brew install anomalyco/tap/opencode

# Or via npm
npm install -g opencode-ai
```

Once installed, navigate to your project directory and run:

```bash
opencode
```

On first launch, run `/init` to have OpenCode analyze your project and generate an `AGENTS.md` file that helps it understand your codebase.

#### Option B: OpenCode Desktop (Beta)

The desktop app provides a graphical interface and is available for macOS, Windows, and Linux.

**macOS (Homebrew):**

```bash
brew install --cask opencode-desktop
```

**Direct download:** Visit <https://opencode.ai/download> to download the installer for your platform:
- macOS (Apple Silicon or Intel) -- `.dmg`
- Windows (x64) -- `.exe` installer
- Linux -- `.deb` or `.rpm`

#### IDE Extensions

OpenCode also offers extensions for VS Code, Cursor, Zed, Windsurf, and VSCodium. See the [IDE documentation](https://opencode.ai/docs/ide/) for setup instructions.

For the full list of installation options and detailed configuration, see the official [OpenCode documentation](https://opencode.ai/docs/).

### Step 3: Log into GitHub Copilot via OpenCode

Once you have your approved Copilot account and OpenCode installed, you must set GitHub Copilot up as your model provider to get access to the premium / flagship models.

### Step 4: Install and Share Useful Tools and Skills

This repository contains shared resources to enhance your OpenCode setup:

- **MCP Servers** -- Model Context Protocol servers for extending agent capabilities
- **OpenCode Configuration Examples** -- Ready-to-use configuration files and templates
- **Plugins** -- Extensions and integrations for OpenCode
- **Skills** -- Reusable agent skills for common workflows

See the [FAQ](faq.md) for common questions.
