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

Remember, your GitHub Copilot username is **yourcecid_cisco** and authentication uses Cisco SSO.

#### Using the Terminal (TUI)

1. Launch OpenCode in your terminal:

   ```bash
   opencode
   ```

2. Run the `/connect` command and select **GitHub Copilot Public**:

   ```
   /connect
   ```

3. OpenCode will display a device code and a URL. Navigate to [github.com/login/device](https://github.com/login/device) in your browser. Log in with your Cisco username (**yourcecid_cisco**) and enter the code shown:

   ```
   ┌ Login with GitHub Copilot
   │
   │ https://github.com/login/device
   │
   │ Enter code: XXXX-XXXX
   │
   └ Waiting for authorization...
   ```

4. After authorizing in your browser, OpenCode will confirm the connection. Run `/models` to select a model:

   ```
   /models
   ```

   You will see a list of available models from GitHub Copilot. Select one to begin your session.

#### Using the Desktop App

1. Open the OpenCode Desktop application.

2. Use the `/connect` command in the chat input and select **GitHub Copilot Public**.

3. The app will display a device code. Open [github.com/login/device](https://github.com/login/device) in your browser, log in with your Cisco username (**yourcecid_cisco**), and enter the code to authorize.

4. Once authorized, use `/models` to select your preferred model from the GitHub Copilot provider.

#### Selecting a Model

After connecting, you can switch between models at any time using the `/models` command. GitHub Copilot provides access to premium models including Claude, GPT, and Gemini families. Some models may require a [GitHub Copilot Pro+ subscription](https://github.com/features/copilot/plans).

For more details on provider configuration, see the [OpenCode Providers documentation](https://opencode.ai/docs/providers/#github-copilot).

### Step 4: Install and Share Useful Tools and Skills

This repository contains shared resources to enhance your OpenCode setup. Browse each directory for setup instructions and a README listing what's available:

- **[MCP Servers](../mcp-servers/)** -- Model Context Protocol servers for extending agent capabilities (Context7, Obsidian, Splunk, NetBox, Kubernetes, Airtable, and more).
- **[Skills](../skills/)** -- Reusable agent skills for common workflows. The [skills README](../skills/README.md) explains how to install them with a natural-language OpenCode prompt and documents which skills depend on each other (e.g. the `cisco-brand` + `pptx` + `deck` presentation bundle).
- **[Docs](../docs/)** -- Additional guides including this getting-started doc and the FAQ.

#### Quick install: skills

The fastest way to install any skill from this repo is to ask OpenCode in plain English, for example:

```
Install the cisco-brand, pptx, and deck skills from
https://github.com/cisco-asp/trusted-ai-toolkit
```

OpenCode will resolve that to the underlying `npx skills add cisco-asp/trusted-ai-toolkit@<skill>` command and register the skills under `~/.agents/skills/`. See the [skills README](../skills/README.md) for the full list and dependency notes.

See the [FAQ](faq.md) for common questions.
