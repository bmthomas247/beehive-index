# The Ledger rebrand: how it gets onto the pages

The site's pages are rebuilt and pushed many times a day by the page builder (the "data refresh" and
"front end" commits). If the rebrand were only edited into the HTML here, the next build would put the
old brand back. So this branch adds the brand files plus one script, and the builder runs the script as
its last step.

## What's in this branch

| Path | What it is |
|---|---|
| `brand/` | Logos, icons, share card, X avatar and header, `tokens.css`, `BRAND.md` (the brand guide) |
| `favicon.svg`, `favicon.ico`, `site.webmanifest` | New root files browsers ask for |
| `apple-touch-icon.png`, `favicon-32.png`, `favicon-48.png` | Replaced with the new mark |
| `_rebrand/apply_rebrand.py` | Applies the rebrand to the finished pages |
| `_rebrand/screenshots/` | Before / after screenshots |

Folders starting with `_` aren't published by GitHub Pages (Jekyll), so `_rebrand/` stays private to the
repo. No page HTML is changed in this branch: the builder's next run does that.

## The one step to add to the builder

After the builder writes the pages and before it pushes them, run (from the repo root):

```
python _rebrand/apply_rebrand.py .
```

If the builder writes the pages in another folder, pass that folder and point `--brand` at this repo's
`brand/` folder:

```
python _rebrand/apply_rebrand.py <folder with the pages> --brand <this repo>/brand
```

- Python 3, standard library only.
- It patches every top-level `*.html` page (190 today). It skips the Google site-ownership file and the
  blank tracking pages in `t/`.
- It changes favicons and manifest links, titles, share-card tags, JSON-LD names, the header logo, news
  labels, footers and colors inside the pages' own `<style>` blocks. It never touches scripts, rankings
  data, stats logic, URLs or school colors.
- Running it again changes nothing, so it's safe to run on every build.
- It prints a JSON summary. `left_unchanged` lists anything it expected to change but couldn't find. That
  is the sign a page's layout changed and the script needs a look.
- `--dry` shows what it would change without writing anything.

## Colors on new parts of the site

Navy turns black everywhere it appears in a page's styles, including panels added later: any dark navy
or blue-slate becomes a neutral charcoal of the same brightness. Brighter blues are left alone, such as
school colors and chart colors like the "pass" bar. The gold stays the site's own `#E8A33D`.

## Undo

Stop running the step. The next build puts the old pages back. To also bring back the old tab icons,
revert this branch's changes to `apple-touch-icon.png`, `favicon-32.png` and `favicon-48.png`.
