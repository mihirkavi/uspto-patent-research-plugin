# README images

Images used by the root `README.md`.

| File | What it is | How it was made |
| --- | --- | --- |
| `banner-light.png`, `banner-dark.png` | Title banner for light and dark mode | Rendered with headless Chromium from `source/banner.html` (one file with a dark-mode media query) |
| `terminal.png` | Terminal card: the server's offline `--self-test` and the offline unit tests | Real output, run without `USPTO_ODP_API_KEY` and without network calls, rendered as a card |

The conceptual cover art lives in `assets/brand/`. The `.github/` folder holds only these presentation files and deliberately has no README of its own, because GitHub would show it instead of the root README.

## Visual identity

Patent-drawing look built on the project's own brand palette (midnight blue, warm copper, archival cream, from `assets/brand/README.md`) and the plugin's brand colour `#1BA5CF`. Patent tools (USPTO's site uses Public Sans and navy; Google Patents and The Lens are clean and blue on white) read as precise and archival. The banner borrows the form of a patent drawing, not any USPTO mark or seal.

- **Fonts:** Spectral (headline), Public Sans (text), IBM Plex Mono (labels and reference numerals). All from Google Fonts.
- **Colours:** cream `#f4eedf` / blueprint navy `#0e1828` background, midnight `#14233c` / cream `#f1e9d6` ink, copper `#a85f2e` (light) / `#d68a55` (dark), lens `#1ba5cf` / `#43d0fb`.
- **Motif:** "FIG. 1", a line drawing of a magnifier over stacked file-wrapper sheets with a copper continuity chain, reference numerals 10 to 18 with lead lines, a drafting-sheet border and a faint grid. Illustration only.
- **README:** badges use `14233c` and `a85f2e`; no emoji in headings.

To re-render after editing `source/banner.html` (needs Node.js with Playwright and a Chromium build):

```bash
node render-html.mjs .github/assets/source/banner.html .github/assets/banner-light.png --scheme light
node render-html.mjs .github/assets/source/banner.html .github/assets/banner-dark.png --scheme dark
```

`render-html.mjs` is a small Playwright script, not part of this repository: it opens the file at 1600x600, sets `prefers-color-scheme`, waits for fonts and saves a 2x screenshot. Any headless browser screenshot at that size works the same way.

Notes for agents: images must never show an API key, account details or unpublished invention material. Use offline output, public records or synthetic examples only. Keep file names stable because the README links to them.
