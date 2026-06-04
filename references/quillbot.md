# QuillBot AI Humanizer driver

URL: `https://quillbot.com/ai-humanizer`
Free word limit: **125 words per run.** Free accounts also have a **daily run cap**
(a "Daily limit reached / Upgrade to Premium" modal) and an occasional
"Sign up to continue Humanizing" wall after a handful of anonymous runs.

## The one thing that trips everyone up

The input is a `contenteditable` editor (React/Slate-style). Writing text into it
with `fill`, `execCommand("insertText")`, or setting `.innerText` puts the characters
on screen **but does not update QuillBot's internal word counter** — it keeps reading
`0 words`, and clicking Humanize then does nothing.

The only input path that syncs the counter is QuillBot's **own "Paste" button**, which
reads the system clipboard. So the reliable cycle is: put text on the clipboard with
`pbcopy`, load a fresh page (so the editor is empty and the Paste button is visible),
click Paste, then Humanize.

The "Paste" button is only rendered when the editor is **empty and unfocused** — i.e.
right after a fresh page load. That's why each chunk starts with a `navigate` reload
rather than trying to clear the box in place (clearing also triggers a "Delete Text"
confirm modal).

## Per-chunk cycle

All commands go through the Kimi WebBridge daemon with the same `session`. Selectors are
**text-based** (button innerText), never `@e` refs — the refs renumber after every
humanize, but the button labels are stable.

1. `pbcopy` the chunk (≤125 words).
2. `navigate` to the URL in the **same tab** (`newTab:false`) to reset to an empty editor.
   Wait ~5s for load.
3. Click the **Paste** button:
   ```js
   (()=>{const b=[...document.querySelectorAll("button")].find(x=>x.innerText.trim()==="Paste");if(!b)return "NOPASTE";b.click();return "ok"})()
   ```
4. Verify the editor now has text (length > 0). If it's still empty, the clipboard read
   was blocked — re-`pbcopy` and retry the Paste click once.
5. Click the **Humanize** button:
   ```js
   (()=>{const b=[...document.querySelectorAll("button")].find(x=>x.innerText.trim()==="Humanize");if(!b)return "NOHZ";b.click();return "ok"})()
   ```
6. Wait ~9s, then read the output. After a run there are **multiple** contenteditables
   (input, output, plus one per output sentence for the diff view). The full humanized
   text is the **second** editor (index 1) on the first run; after re-humanizing it can
   shift, so prefer reading the editor whose text differs from the input and is longest:
   ```js
   (()=>{const e=[...document.querySelectorAll("[contenteditable]")].map(x=>x.innerText.trim());return JSON.stringify(e)})()
   ```
   Take the longest entry that is not the input and not a single sentence. Ignore any
   trailing duplicate sentence — QuillBot's diff view sometimes appends one.

## Recovery states (check the buttons / a screenshot when output is empty)

- **"Try again" button present** → transient server error. Click it, wait, re-read.
  This happens intermittently and almost always succeeds on the second try.
- **"Continue with Google / Apple / Facebook" or "Create account"** → signup wall.
  **Stop and ask the user** to log in (or switch account), then resume. Do not fake output.
- **"Daily limit reached" / "Upgrade now" modal** → daily cap. **Stop and ask the user**:
  switch QuillBot account, wait for reset, or try a different humanizer. Never pay/upgrade
  on the user's behalf and never write the humanized text yourself.
- **"Delete Text" confirm modal** (only if you tried to clear in place) → check
  "Don't show again" and click Continue. Avoid this by reloading instead of clearing.
