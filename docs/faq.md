# Frequently Asked Questions

**Q: Can't I just use GitHub Copilot as my model provider in Claude Code / Co-Work / Claude Desktop?**

A: While there is technically a workaround / hack for this, Anthropic's tool calling does not work reliably with other model providers.

**Q: Can I use another model provider with OpenCode?**

A: Yes. However, they may not be approved for Cisco data. One of the many advantages of using this setup is being able to select the models and model providers within any given session.

**Q: I have a GPU running a model locally (Ollama + DGX Spark, Jetson, Mac Mini, etc). Can I use OpenCode with GitHub Copilot and also use my local model?**

A: Absolutely. You can add multiple providers and use the `/models` selection to switch between them.
