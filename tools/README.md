# Tools

## `build_packet.py`

Builds all three packets in `papers/` from the Markdown in `docs/`:

```bash
python tools/build_packet.py
```

Requires `reportlab` and Arial Unicode MS (override the font path with
`DEKSIRIP_FONT`). `pypdf` and `PyMuPDF` are optional: with them the script
verifies each packet and writes QA images to `local/private/pdf-qa/`, without
them it only writes the PDFs.

A packet is five pages built from five blocks with a forced page break between
them:

1. `model-at-a-glance` up to "what is common";
2. the rest of `model-at-a-glance`;
3. `concept-note` up to §4;
4. `concept-note` from §4;
5. the closing page — questions, sources, contact — which lives in `END` in the
   script because it exists only in the packet.

Three things explain the shape of the output:

- the concept note's scope section (§8) is dropped and its version line removed,
  because the packet carries its own title and date on page 1;
- block quotes (`> 翻译说明…`) render as the small grey note that states a text
  is machine translated;
- forcing a break before each block is why page 1 ends with white space.

The English and Russian packets in `papers/` were rebuilt with this script from
unchanged sources and reproduce the published files page for page, so the
styling — 19 mm margins, 19 / 12 / 10 / 9 / 8 pt, navy `#17324D` headings — is
the original, not an approximation.
