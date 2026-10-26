# README images

Images used by the root `README.md`.

| File | What it is | How it was made |
| --- | --- | --- |
| `banner-light.png`, `banner-dark.png` | Title banner for light and dark mode | Rendered from an HTML template with headless Chromium |
| `terminal.png` | Terminal card: the server's offline `--self-test` and the offline unit tests | Real output, run without `USPTO_ODP_API_KEY` and without network calls, rendered as a card |

The conceptual cover art lives in `assets/brand/`. The `.github/` folder holds only these presentation files and deliberately has no README of its own, because GitHub would show it instead of the root README.

Notes for agents: images must never show an API key, account details or unpublished invention material. Use offline output, public records or synthetic examples only. Keep file names stable because the README links to them.
