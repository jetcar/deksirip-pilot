# Tools

## `build_packet_zh.py`

Rebuilds [`papers/concept-note-zh.pdf`](../papers/concept-note-zh.pdf) from
[`docs/model-at-a-glance-zh.md`](../docs/model-at-a-glance-zh.md) and
[`docs/concept-note-zh.md`](../docs/concept-note-zh.md).

```bash
python tools/build_packet_zh.py            # writes papers/concept-note-zh.pdf
python tools/build_packet_zh.py out.pdf    # or somewhere else
```

Requirements: `pip install reportlab`, and the Arial Unicode MS font — the same
one the published packets embed. Set `DEKSIRIP_FONT` to its path if it is not in
a standard location.

The Russian and English packets were produced by the author's
original tool, which is not in this repository. This script reproduces the
Chinese packet's geometry from measurements of that output — A4, text left at
59.86 pt, frame width 477.1 pt, footer at 34 pt, 19 / 12 / 10 / 9 / 8 pt on a
20 pt grid, headings in `#172F4D` — so a rebuilt Chinese packet looks like the
other two rather than like a different document.

Three things are deliberate:

- the cover carries one translation note, so a five-page file states its
  provenance once instead of repeating it after every heading;
- block quotes from the sources (`> 翻译说明…`) are skipped for that reason;
- the page-5 block — questions, sources, contact — is text in this script, not
  in the Markdown sources, because it exists only in the packet.

The output is close to, not byte-identical with, the original tool's files.
Page breaks may fall differently; content and styling do not.
