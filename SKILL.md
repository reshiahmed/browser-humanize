---
name: browser-humanize
description: >-
  Humanize AI-written text by driving a real online humanizer tool (QuillBot AI
  Humanizer, Grammarly Humanizer, ZeroGPT, Undetectable.ai, etc.) in the user's
  browser via Kimi WebBridge — pasting the text in chunks within the tool's word
  limit and collecting the genuinely tool-produced output. Use this whenever the
  user wants to "humanize" / "make text sound human" / "bypass AI detection" /
  "remove AI tells" USING A SPECIFIC WEBSITE OR TOOL, names a humanizer site, or
  asks to run their writing (an essay, thesis, blog post, email, report) through
  one of these tools. Also trigger when the user says "humanize this with
  QuillBot/Grammarly", "paste my text into the humanizer", or "run it through the
  AI humanizer and give me the output". The user supplies the text and which tool;
  if they don't give the word limit, find it. Prefer this over rewriting the text
  yourself — the user specifically wants the external tool's output, not your prose.
---

# Browser Humanize

Drive an online humanizer tool in the user's real browser and return its output.
The user picks the tool and provides the text; this skill handles opening it,
pasting in chunks under the tool's word limit, recovering from the tool's quirks,
and assembling the humanized result.

**Core promise: the output must come from the tool.** Never rewrite or hand-write
the "humanized" text yourself — that defeats the entire purpose and misleads the
user. If the tool blocks you (login wall, daily limit, captcha), stop and ask the
user how to proceed; don't paper over it.

## Inputs to gather

1. **The text** to humanize (from the user, a file, or earlier in the conversation).
2. **The tool** — QuillBot, Grammarly, or another humanizer site.
3. **The word limit per run** — ask the user first; many know it (QuillBot free = 125).
   If they don't, discover it (see the reference files). Tell them the limit you'll use.

If any of these is missing, ask — but don't over-interview. The tool and text are
usually obvious from the request.

## Workflow

### 1. Health-check the browser bridge

```bash
~/.kimi-webbridge/bin/kimi-webbridge status
```

If it's not `running: true` + `extension_connected: true`, the `kimi-webbridge` skill's
`references/operations.md` has the fix. The bridge is required — this skill is entirely
browser automation.

### 2. Load the tool recipe

- **QuillBot** → read `references/quillbot.md` (the best-supported, fully-automatable tool).
- **Grammarly** → read `references/grammarly.md` first — its editor can't be automated,
  so you'll likely steer the user to QuillBot or a manual paste loop.
- **Anything else** → read `references/generic-tool.md` and discover its mechanics live.

Each recipe explains the one detail that makes or breaks this: humanizer inputs are
usually `contenteditable` editors that **ignore programmatically-inserted text** — their
word counter stays at 0 and the action button does nothing. The fix (clipboard + the
site's own Paste button, on a freshly-loaded page) is in the recipe. Don't skip it.

### 3. Chunk the text under the limit

Use the bundled splitter so sentences are never cut and runs are minimized:

```bash
python scripts/chunk_text.py <limit> <input_file>     # or pipe text via stdin
```

It returns a JSON list of chunks, each ≤ the limit, packed sentence-by-sentence and
respecting paragraph breaks. Keep a record of which chunk maps to which part of the
source so the output reassembles in order.

### 4. Humanize each chunk

Use one Kimi WebBridge `session` for the whole job (e.g. `humanize-<thing>`). For each
chunk, follow the per-chunk cycle in the tool's recipe. The shape is always:

> `pbcopy` the chunk → fresh-load the tool page → paste via the site's Paste button →
> verify the counter registered the text → click the action button → wait → read the
> output editor → record the humanized chunk.

After each run, **verify** you actually got new output (not an empty box, not the
unchanged input). If it's empty, check for a "Try again" button (transient error —
click and retry) or a wall/limit modal (stop and ask the user). The recipes list the
exact recovery states.

Process chunks one at a time. A second browser tab does **not** bypass a daily limit —
the cap is account-wide — so don't bother parallelizing for that reason.

### 5. When you hit the limit, ask — don't push through

The moment a tool throws a signup wall or "daily limit reached" modal, **stop and report
which chunks are done and which aren't**, then ask the user how to continue. Typical
options to offer: log in / switch account, wait for the daily reset, or switch to another
humanizer. Resume from the next unfinished chunk once they answer. This is a feature, not
a failure — the user told you to stop at limits rather than fabricate output.

### 6. Deliver both files + the text

Save two markdown files (default under `/tmp/`, or next to the source file if the input
came from one) so the user can diff old vs new:

- `*-original.md` — the input text, chunked under the same headings.
- `*-humanized.md` — the assembled humanized output, in source order.

Then print the full humanized text in the chat. If the text originally came from a file
and the user wants it written back, do that too — but only on request; don't silently
overwrite their source.

Close the Kimi session (`close_session`) once the user has what they need, unless they
might want to keep iterating in the same tab.

## Reference files

- `references/quillbot.md` — QuillBot AI Humanizer (125-word free limit, full automation).
- `references/grammarly.md` — Grammarly Humanizer (cannot be automated; manual path).
- `references/generic-tool.md` — discovering and driving any other humanizer site.
- `scripts/chunk_text.py` — sentence-aware splitter that keeps chunks under the limit.
