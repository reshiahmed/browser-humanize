# Driving a humanizer the skill doesn't have a recipe for

If the user names a tool with no reference file (ZeroGPT humanizer, Undetectable.ai,
HIX Bypass, Humbot, etc.), discover its mechanics live rather than guessing. The same
principles from `quillbot.md` apply almost everywhere.

## Discovery sequence

1. `navigate` to the tool's humanizer page, wait for load, `snapshot` it.
2. Find the **input editor** (a `textarea` or `[contenteditable]`) and the **action
   button** (labelled Humanize / Rewrite / Bypass / Paraphrase).
3. Find the **word/character limit**. First ask the user — they often know it. If not,
   look for: a counter near the input ("0 / 500 words"), a limit note, or the pricing
   page ("up to N words free"). If you still can't tell, probe: paste a ~120-word chunk
   and humanize; if it works, try ~250; binary-search the ceiling. Tell the user the
   limit you found.

## Input method — try in this order, stop at the first that updates the counter

The goal is to get the tool's **own word counter** to reflect the text, because that's
what its button reads. Watch the counter (snapshot or screenshot) after each attempt.

1. **Plain `textarea`**: the `fill` tool works directly and fires input events. Usually
   enough. Verify the counter moved.
2. **`contenteditable` with a "Paste" button**: `pbcopy` the chunk, reload for a clean
   editor, click the site's Paste button (reads clipboard, fires the right events). This
   is the QuillBot pattern.
3. **`contenteditable`, no Paste button**: focus it and `execCommand("insertText", ...)`.
   Sometimes registers, sometimes not.
4. If none move the counter, the editor likely enforces trusted events (see
   `grammarly.md`). Fall back to the **user-in-the-loop** path: hand the user each chunk
   to paste manually and report the result back.

## Selectors

Use **text-based / role-based selectors** (button innerText, textarea by placeholder),
not `@e` refs — single-page humanizer apps renumber refs after every run.

## Output

Read the result editor/panel after the action completes (allow ~8-12s). On diff-style
tools, read the assembled output, not the per-sentence fragments. Strip any duplicated
trailing sentence.

## Always stop and ask — never fake

If you hit a login wall, paywall, captcha, daily-limit modal, or persistent failure,
**stop and ask the user how to proceed** (log in, switch account, wait, change tool).
Never invent or hand-write the "humanized" text — the entire point is that it came from
the tool. If you wrote it yourself it would defeat the purpose and mislead the user.
