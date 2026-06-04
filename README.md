# browser-humanize

A [Claude Code](https://claude.com/claude-code) / Claude Agent skill that humanizes AI-written text by driving a **real online humanizer tool** in your own browser via [Kimi WebBridge](https://www.kimi.com/features/webbridge) — rather than rewriting the prose itself.

It pastes your text in chunks within each tool's word limit and collects the genuinely tool-produced output.

## Supported tools

- Grubby AI
- HumanizeAI Pro
- HumanizeAI (free)
- QuillBot AI Humanizer
- Grammarly Humanizer
- ZeroGPT
- Undetectable.ai
- Other generic humanizer sites

All of these have free tiers. The skill works down the list best-first: it uses one tool until its limit is hit, then moves to the next, chaining through all of them. A subscription on any tool raises (or removes) that limit, so you stay on the better tool longer before falling through.

## How it works

1. You supply the text and which tool to use.
2. The skill opens the tool in your real browser session (your logins, your subscription).
3. It splits the text into chunks under the tool's word limit (`scripts/chunk_text.py`).
4. It pastes each chunk, runs the humanizer, and collects the real output.

Tool-specific notes live in [`references/`](references/).

## Install

Drop this folder into your skills directory:

```bash
git clone https://github.com/reshiahmed/browser-humanize.git \
  ~/.claude/skills/browser-humanize
```

The skill auto-loads on next session. Requires the Kimi WebBridge browser daemon and the Chrome extension:

- **Kimi WebBridge — Chrome Web Store:** https://chromewebstore.google.com/detail/kimi-webbridge/fldmhceldgbpfpkbgopacenieobmligc

## Structure

```
SKILL.md              # skill manifest + instructions
scripts/chunk_text.py # word-limit chunking helper
references/           # per-tool guidance (QuillBot, Grammarly, generic)
```

## License

MIT
