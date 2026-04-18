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

Download and install from here:
<https://opencode.ai/download>

### Step 3: Log into GitHub Copilot via OpenCode

Once you have your approved Copilot account and OpenCode installed, you must set GitHub Copilot up as your model provider to get access to the premium / flagship models.

### Step 4: Install and Share Useful Tools and Skills

This repository contains shared resources to enhance your OpenCode setup:

- **MCP Servers** -- Model Context Protocol servers for extending agent capabilities
- **OpenCode Configuration Examples** -- Ready-to-use configuration files and templates
- **Plugins** -- Extensions and integrations for OpenCode
- **Skills** -- Reusable agent skills for common workflows

## FAQ

**Q: Can't I just use GitHub Copilot as my model provider in Claude Code / Co-Work / Claude Desktop?**

A: While there is technically a workaround / hack for this, Anthropic's tool calling does not work reliably with other model providers.

**Q: Can I use another model provider with OpenCode?**

A: Yes. However, they may not be approved for Cisco data. One of the many advantages of using this setup is being able to select the models and model providers within any given session.

**Q: I have a GPU running a model locally (Ollama + DGX Spark, Jetson, Mac Mini, etc). Can I use OpenCode with GitHub Copilot and also use my local model?**

A: Absolutely. You can add multiple providers and use the `/models` selection to switch between them.
