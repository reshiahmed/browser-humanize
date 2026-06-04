# Grammarly — known limitation

URL: `https://app.grammarly.com/` (redirects to the Coda-based editor at
`coda.grammarly.com/d/...`). It has a right-side **"Humanizer"** panel.

**Grammarly's editor cannot be driven by browser automation.** It uses a Slate-based
editor that only updates its internal model from *trusted* keyboard/input events. Text
inserted via `fill`, `execCommand("insertText")`, paste-button clicks, or direct DOM
writes appears on screen but the word counter stays at `0 words` and the Humanizer panel
reports "Not enough content — write or paste at least 8 words." There is no programmatic
workaround — this is the `isTrusted` event boundary that the Kimi WebBridge skill calls
out as a hard product limit (no automation that runs without stealing OS focus can forge
trusted events on such editors).

**So:** if the user asks for Grammarly, explain this up front and offer the
**user-in-the-loop** path: you give them the exact chunk text, they paste it into the
open Grammarly doc, click Humanizer, apply, and paste the result back to you. Or suggest
QuillBot, which automates cleanly. Don't burn time trying to force Grammarly's editor.
