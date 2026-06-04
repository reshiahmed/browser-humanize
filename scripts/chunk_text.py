#!/usr/bin/env python3
"""Split text into chunks that stay under a word limit, keeping sentences whole.

Why this exists: humanizer sites cap free runs at N words (QuillBot free = 125).
Pasting more than the cap silently fails (the box stays empty / counter shows the
cap). So we pack whole sentences into chunks just under the limit, never cutting a
sentence in half, and keep paragraph boundaries so the output maps back cleanly.

Usage:
    python chunk_text.py <limit> <infile>      # reads file
    echo "text" | python chunk_text.py <limit> # reads stdin

Prints a JSON list of chunk strings.
"""
import sys, json, re


def split_sentences(paragraph):
    # Split on sentence enders followed by whitespace. Good enough for prose;
    # abbreviations may over-split but that only costs an extra (harmless) run.
    parts = re.split(r'(?<=[.!?])\s+', paragraph.strip())
    return [p for p in parts if p]


def chunk(text, limit):
    chunks = []
    for para in re.split(r'\n\s*\n', text.strip()):
        para = para.strip()
        if not para:
            continue
        cur, cur_words = [], 0
        for sent in split_sentences(para):
            n = len(sent.split())
            if n > limit:
                # A single sentence longer than the limit: flush what we have,
                # then hard-split this sentence by words as a last resort.
                if cur:
                    chunks.append(' '.join(cur)); cur, cur_words = [], 0
                words = sent.split()
                for i in range(0, len(words), limit):
                    chunks.append(' '.join(words[i:i + limit]))
                continue
            if cur_words + n > limit:
                chunks.append(' '.join(cur)); cur, cur_words = [], 0
            cur.append(sent); cur_words += n
        if cur:
            chunks.append(' '.join(cur))
    return chunks


def main():
    if len(sys.argv) < 2:
        print("usage: chunk_text.py <word_limit> [infile]", file=sys.stderr)
        sys.exit(1)
    limit = int(sys.argv[1])
    if len(sys.argv) >= 3:
        with open(sys.argv[2]) as f:
            text = f.read()
    else:
        text = sys.stdin.read()
    print(json.dumps(chunk(text, limit)))


if __name__ == '__main__':
    main()
