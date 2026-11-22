# The Ledger · brand guide

**The Ledger** leads. **Utah High School Football** is the descriptor. The voice is data-driven, authoritative and independent. The colors are **black and gold**.

## The mark

The state of Utah, with **THE** and **LEDGER** cut out of it and a football lace on a slant between them. The name sits inside the mark, so the words beside it can simply say what the site covers: UTAH HIGH SCHOOL over FOOTBALL.

- **Utah's shape** follows the state's own border description: Utah Constitution, Article II, Section 1 ([le.utah.gov](https://le.utah.gov/xcode/ArticleII/UC_AII_S1_1800010118000101.html)). The state is 5 degrees of latitude by 5 degrees of longitude. The Wyoming step takes 2/5 of the width and 1/5 of the height. At Utah's latitude that makes the state about 0.79 as wide as it is tall.
- **The lace** is the football. It also sits where a bookkeeper's total line would go, between the heading and the name.
- **No big single letter in the mark.** An earlier version carved a large "L" into the state, and at a glance it read as "Utah takes an L" (a loss). Spelling out the words avoids that.

The mark is drawn on a 48-unit grid. In the full mark the state runs from x 9 to 42 and from y 3 to 45.

### Black and gold, both ways

| On | The state | THE, LEDGER | The lace |
|---|---|---|---|
| Light backgrounds | Black | Cut out (the background shows) | Gold |
| Dark backgrounds | Gold | Cut out (the background shows) | Cut out |

On dark backgrounds the whole state turns gold and the lace is cut out with the words, so the mark is one solid gold shape. (We tried bright yellow `#FFC72C` and a darker gold first; on Nov 18, 2026 Brandon picked the gold already in the site's header, `#E8A33D`.)

### Two sizes of mark

| Version | Use at | What it is |
|---|---|---|
| Full mark (`icon`) | 48 px tall and up | State, THE, LEDGER and the slanted lace |
| Small mark (`icon-small`) | 16–32 px (browser tabs, tiny UI) | State and a straight lace, drawn on the pixel grid, no words |

The words can't be read below about 48 px, and a slanted line blurs at 16 px, so the small mark keeps only the shape and a lace that lands on whole pixels. Never shrink the full mark below 48 px; switch to the small one instead.

## Files

Everything lives in `/brand`. All type in the logo files is converted to outlines, so the files don't depend on any installed font.

| What | File | Use it for |
|---|---|---|
| Horizontal lockup (primary) | `logo/ledger-horizontal-*.svg` | Site header, documents, anything wide |
| Stacked lockup | `logo/ledger-stacked-*.svg` | Square or tall spaces, social posts, merch |
| Full mark | `logo/ledger-icon-*.svg` | Avatars, app icons, watermark (48 px and up) |
| Small mark | `logo/ledger-icon-small-*.svg` | 16–32 px only |
| Wordmark | `logo/ledger-wordmark-*.svg` | Text-only spots where the mark can't go |
| Favicon (follows light/dark) | `/favicon.svg` | Browser tabs (modern browsers) |
| Favicon fallback | `/favicon.ico` (16, 32, 48), `/favicon-32.png`, `/favicon-48.png` | Older browsers, Safari |
| iOS home screen | `/apple-touch-icon.png` (180 × 180) | Linked from every page |
| Android / install | `icons/icon-192.png`, `icons/icon-512.png` (safe for round masks) | `/site.webmanifest` |
| Share card | `social/og-card-1200x630.png` | `og:image` and `twitter:image` on every page |
| X avatar | `social/x-avatar-400.png` | @TheLedgerUT profile picture |
| X header | `social/x-header-1500x500.png` | @TheLedgerUT banner |
| Colors and type | `tokens.css` | CSS variables (see below) |

Each logo comes in four versions:

| Version | Use on |
|---|---|
| `color-on-dark` | Ledger Black `#0e1116`, the site's top bar and other dark backgrounds |
| `color-on-light` | White or light backgrounds |
| `white` | Photos and busy dark backgrounds, one-color printing |
| `black` | One-color printing, stamps, faxes, embroidery |

In the white, black and color-on-dark versions the lace is cut out of the state, so it shows in one color. Each social image has an SVG master next to it. `work/build_brand2.py` rebuilds every file, and `brand/preview.html` shows them all.

## Clear space

Keep empty space around the logo equal to **the height of the letters in LEDGER** (about a sixth of the state's height) on every side. Nothing goes inside that space: no text, no edges, no other logos.

## Minimum sizes

| Logo | Smallest on screen | Smallest in print |
|---|---|---|
| Horizontal lockup | 48 px tall | 1.25 in (32 mm) wide |
| Stacked lockup | 120 px tall | 1 in (25 mm) wide |
| Full mark | 48 px tall | 0.5 in (13 mm) tall |
| Small mark | 16 px | 0.25 in (6 mm) |
| Wordmark | 18 px tall | 0.75 in (19 mm) wide |

## Colors

| Token | Hex | Use | Contrast |
|---|---|---|---|
| `--ledger-ink` (Ledger Black) | `#0e1116` | Dark base, the top bar; the state on light backgrounds | 18.4:1 on paper |
| `--ledger-gold` (Ledger Gold) | `#E8A33D` | The mark on dark, the lace, FOOTBALL on dark, accents on black | 8.8:1 on black |
| `--ledger-gold-light` (Gold Light) | `#C97A12` | FOOTBALL in the logo on white, big gold type on light | 3.3:1 on paper |
| `--ledger-gold-deep` (Gold Deep) | `#9A6206` | Small gold text on light backgrounds | 5.0:1 on paper |
| `--ledger-chalk` | `#F2F4F6` | UTAH HIGH SCHOOL and type on dark | 17.2:1 on black |
| `--ledger-paper` | `#FBFCFC` | Light base | |
| `--ledger-slate` | `#4A5560` | Quiet type, on light | 7.4:1 on paper |
| `--ledger-slate-bright` | `#A3AFB9` | Quiet type, on dark | 8.5:1 on black |

Contrast follows the WCAG formula. **Ledger Gold on white is only 2.1:1**, so on light backgrounds FOOTBALL in the logo uses Gold Light (3.3:1) and small text uses Gold Deep (5.0:1). Black text on Ledger Gold is 8.8:1, so gold buttons and tags take black text. All three golds were already on the site (header, light-mode accents).

`tokens.css` also has role variables (`--ledger-fg`, `--ledger-accent`, `--ledger-muted`, `--ledger-bg`). They switch with `prefers-color-scheme` and the site's `data-theme` attribute, the same way the site's own colors do.

## Type

| Role | Font | Weight | Setting |
|---|---|---|---|
| THE / LEDGER in the mark | Saira Condensed | ExtraBold 800 | All caps, +0.01em |
| UTAH HIGH SCHOOL / FOOTBALL | Saira Condensed | ExtraBold 800 | All caps, +0.01em; FOOTBALL about 1.45× the size of the first line, in gold (Gold Light on white) |
| Supporting lines (taglines, URLs) | Saira Condensed | Bold 700 | Sentence case |

Saira Condensed is under the SIL Open Font License 1.1 and free on Google Fonts. The logo files contain outlines, not live text, so nothing needs to load for the logo to show. The site's own reading font (Archivo) doesn't change.

## Do

- Use the files as they are: scale them, don't rebuild them.
- Pick the version that matches the background (light, dark, white, black).
- Use the small mark at 32 px and under, the full mark at 48 px and up.
- Keep to black and gold. Gold is the one accent.
- Keep the clear space and minimum sizes above.

## Don't

- Stretch, squash, tilt or rotate the logo, or redraw the state's outline.
- Put a single big letter back into the state (it reads as "an L").
- Straighten the lace on the full mark, or slant it on the small mark.
- Recolor the logo in anything but black, gold, white or one print color.
- Use Ledger Gold for words on white (use Gold Light for big type, Gold Deep for small).
- Set THE LEDGER in another font, or retype it as live text in place of the logo.
- Put the logo on a busy photo without the white version and enough contrast.
- Add effects: shadows, glows, outlines, gradients.
- Put the logo on or next to school, UHSAA, college or NFL marks in a way that suggests a partnership. The site is independent.

## On the site

| Where | What shows |
|---|---|
| Top bar (app and program pages) | Ledger Black with a gold line under it (was navy) |
| App top bar logo | Full mark at 48 px (phones and narrower windows); the horizontal lockup from 1320 px wide, where the whole menu still fits |
| Program page top bar logo | Full mark at 48 px; the horizontal lockup from 1280 px wide |
| Accents (labels, numbers, bars) | Gold Deep in light mode, Ledger Gold in dark mode and on black panels |
| Dark mode | Neutral blacks on every page (the program pages were blue-gray) |
| Browser tabs | Small mark (favicon) |
| Plain crawlable pages | Horizontal lockup; the light or dark version follows the reader's setting |
| Latest News items written by us | Small mark tile and the label "The Ledger" (were the old football icon and "UHSFB") |
| Titles | "… \| The Ledger · Utah High School Football"; the homepage title starts with it |
| Footers | "The Ledger · Utah High School Football" |

`theme-color` stays `#0e1116` (Ledger Black). School colors on team pages don't change.

## Before anything ships on merchandise

The mark is an original drawing, but state outlines are common in sports logos, and black and gold is a common team pairing. This check isn't a legal clearance. Run a USPTO trademark search (and talk to a lawyer if anything comes close) before the logo goes on apparel or anything sold.
