# Terminal — Style Reference
> A tiling-WM desktop in one browser tab: a waybar on top, a file explorer on the left, a vim buffer in the middle, a statusline at the bottom.

**Themes:** `hypr` (default dark) · `claro` · `e-ink` · `sakura` · `bosque` · `ámbar crt`

The study app (notes + exams) should feel like a terminal tool, not a web page. The references are a Hyprland desktop with vanilla waybar, nvim with a NERDTree-style side panel, htop, and neofetch. Every glyph is JetBrains Mono. Surfaces are flat and there are no shadows. Hierarchy comes from background steps and ANSI color, never from font size: headings in a note are barely larger than body text and are told apart by color, the way a terminal colors markdown.

Two surfaces carry all the chrome. The **waybar** (top) holds navigation and tools. The **statusline** (bottom) holds state and view controls. The content between them stays quiet.

## Layout

```
┌ waybar ─────────────────────────────────────────────────────────────┐
│ [book] (1 notas)(2 exámenes)      lun 21 sept  14:32      [tools][tema▾] │
├──────────────┬──────────────────────────────────────────────────────┤
│┌ explorer ┐  │   notes ~/temas/x ❯ nvim notas/                      │
││ ⌄ tema-a/ 2│  │   Title                                             │
││   recursos/│  │   # subtitle                                        │
││   notas/   │  │ 1 1. Heading                                        │
││ ⌄ tema-b/ 4│  │ 2 paragraph…                                        │
│└───────────┘  │ ~                                                    │
├──────────────┴──────────────────────────────────────────────────────┤
│ NORMAL ~/notes/temas/x/notas     guardado  🔍 − 100% +  ↔ − 736px +  utf-8  Top │
└─────────────────────────────────────────────────────────────────────┘
```

- The page scrolls as a document. The waybar is `position: sticky`, the explorer is sticky under it, and the statusline is `position: fixed`. There is no inner scroll container. The notes editor positions margin cards and menus against `scrollY`, so keep it that way.
- The content column is centered in the panel: `max-width: calc(var(--ancho) + 2 * var(--gutter))`, with symmetric gutter padding. `--ancho` is set from the statusline (defaults: 736px for notes, 960px for exams).
- The content zoom (statusline 🔍) applies CSS `zoom` to `#app` only. Chrome, explorer and bars never zoom. Any code that mixes `clientX/Y` with `offsetLeft/Top` inside `#app` must divide by the zoom (see card drag in `notas.html`).
- Below 900px the explorer hides, the clock hides, and workspace labels collapse to numbers. Below 1280px margin cards stop floating and sit inline.

## Tokens — Colors

Each theme defines the same 20 tokens: an 11-step neutral ramp, an accent, seven ANSI hues and `--on-accent`. Components only read tokens, so a new theme is one CSS block.

| Token | Role |
|---|---|
| `--color-void` | Waybar, statusline, floating menus. The darkest surface |
| `--color-carbon` | Page background (`--papel`) |
| `--color-graphite` | Waybar modules, cards, hover rows |
| `--color-iron` | Hairlines (`--linea`), control fills, hover inside modules |
| `--color-slate` | Explorer frame, line numbers, `~` filler, empty placeholders |
| `--color-pewter` … `--color-ash` | Intermediate steps, rarely used directly |
| `--color-steel` | Heading counters, `//` and `#` prefixes |
| `--color-fog` | Secondary text (`--gris`) |
| `--color-chalk` | Tree items, clock, statusline modules |
| `--color-paper` | Primary text (`--tinta`) |
| `--color-accent` | Active workspace, selected tree node, hovered table row, links, refs, focus rings |
| `--ansi-red` | Failure: wrong answer, save error, recording mic (`--mal`) |
| `--ansi-green` | Success: correct answer, INSERT mode, caret, h3 (`--bien`) |
| `--ansi-yellow` | NORMAL mode, italics, h4, current exam in the tree |
| `--ansi-blue` | h1, folder names in the tree |
| `--ansi-magenta` | Topic type (`libro`, `certificación`), prompt `❯`, h5 |
| `--ansi-cyan` | h2, htop table header, secondary keys, tree subfolders |
| `--ansi-orange` | List markers, `[01]` question numbers, inline `code` |
| `--on-accent` | Text on any filled accent/ANSI background |

The old names (`--papel`, `--tinta`, `--gris`, `--linea`, `--acento`, `--bien`, `--mal`) are aliases kept so page-level CSS stays short. `viz.js` reads the ramp for Mermaid, so diagrams follow the theme.

### Themes

| Key | Name | Character | Carbon | Paper | Accent |
|---|---|---|---|---|---|
| `hypr` | hypr | Navy Hyprland desktop. Default when the OS is dark | `#181c23` | `#dde2ea` | `#4d8fd6` |
| `claro` | claro | Cool light grey. Default when the OS is light | `#f2f4f7` | `#1b2029` | `#2f72bf` |
| `eink` | e-ink | Monochrome dark. Every ANSI hue is a grey; hierarchy comes from lightness only | `#141414` | `#e6e6e6` | `#d4d4d4` |
| `sakura` | sakura | Plum-black neutrals with pastel pink, lavender and mint | `#1b151b` | `#f3e6ee` | `#f2a7c3` |
| `bosque` | bosque | Deep green-grey with sage and moss | `#141b17` | `#e1eadf` | `#8cc68a` |
| `ambar` | ámbar crt | Amber phosphor monitor. Everything is a shade of amber | `#130e06` | `#ffbf57` | `#ffb347` |

Theme selection lives in `tema.js`. `data-tema` on `<html>` picks the block; with no value, the page follows `prefers-color-scheme` (`hypr` or `claro`). The choice persists in `localStorage.tema`. The legacy value `oscuro` maps to `hypr`. Light themes set `color-scheme: light`; everything else inherits `dark`.

To add a theme: copy one `:root[data-tema="…"]` block in `estilo.css`, change the 20 values, and add the key to `TEMAS` in `tema.js`. Check two contrasts: `--on-accent` on `--color-accent` and on `--ansi-cyan` (htop header, keys), and `--color-fog` on `--color-carbon`.

Highlight colors for marks (`COLORES` in `notas.html`) are fixed hexes stored in the `.md`, so they don't change with the theme.

## Tokens — Typography

**JetBrains Mono** for everything: chrome, body, headings, tables, buttons. Weights 400 and 700.
The note body has a reader-font switch (`mono` default, `serif`, `inter`) that only affects `.doc` text. Headings stay mono.

| Role | Size | Notes |
|---|---|---|
| Chrome (waybar, tree, tables) | 13px | |
| Statusline, counts, captions | 12px | |
| Body | 14px / 1.71 | 15px when the reader font is serif or inter |
| Page title (`.portada h1`, exam title) | 22px bold | The only "big" text |
| Note h1 / h2 / h3–h5 | 17 / 15 / 14px bold | Colored blue / cyan / green / yellow / magenta |

Headings are numbered by CSS counters (`1.`, `1.1`, `1.1.1`) and the numbers are not saved to the `.md`.

## Components

### Waybar
`--color-void` bar, 44px tall, three columns (`1fr auto 1fr`).
- **Left:** book icon in accent, then the workspace module: pill links `1 notas` / `2 exámenes`. The active one is filled with accent and `--on-accent` text.
- **Center:** clock, bold `--color-chalk`, `lun 21 sept   14:32`, 24h, updated every 15s. No decoration.
- **Right:** tool modules, then the theme `<select>`. Each module is a `--color-graphite` rounded rect (radius 8px, 30px tall) holding 24px-tall borderless buttons that hover to `--color-iron`. Pressed buttons fill with accent. Color swatches are 12px circles; the pressed one gets a 1.5px outline ring.
- Tools overflow by horizontal scroll with no scrollbar. They never wrap.

### Explorer
Sticky left column, 18rem wide, inside a 1px `--color-slate` frame with an inverted `explorer` title notch (paper background, carbon text) sitting on the top border, like a TUI panel.
- The tree is built from native `<details open>` per topic. The summary is `slug/` in `--ansi-blue` with a count on the right and a `›`/`⌄` marker. The current topic's summary is filled with accent.
- **Notes, current topic:** a `recursos/` subfolder (files with size on the right, links with `↗`), then `notas/` with the live, foldable heading index.
- **Notes, other topics:** their h1 sections as `?tema=slug#id` links, so you can jump between projects without going back to the index.
- **Exams:** each topic lists its exam files. The open exam is `--ansi-yellow`.
- Long names truncate with an ellipsis; the full name is in `title`.

### Content panel
- **Prompt line** above the content: `notes ~/path ❯ command`. Host in green bold, path in blue, `❯` in magenta. It says what the view is (`ls -l`, `nvim notas/`, `exam x.json`, `exam --check`).
- **Line-number gutter:** every top-level block and every list item gets a CSS counter in `--color-slate`, right-aligned in the left gutter. Figures and margin cards are skipped.
- **`~` filler:** eight tildes after the content, like an empty vim buffer.

### htop table
The topic index for both pages. The header row is `--ansi-cyan` with `--on-accent` uppercase labels. Rows are 13px. On hover the whole row fills with accent and all text turns `--on-accent`. Zero counts use `--color-steel`. The topic type uses magenta. Exams hang under their topic as `└─` rows.

### Statusline
Fixed, 24px, `--color-void`, 12px text. Left to right:
- **Mode block:** `NORMAL` (yellow) or `INSERT` (green), bold `--on-accent` text. Notes switch on editor focus. Exams show `INSERT` once any option is picked, then `PASS` or `FAIL` after grading.
- **Path** in `--color-chalk`.
- **Right cluster:** save or progress status, zoom control (magnifier, `−`, numeric %, `+`; 50–250, step 10), width control (`↔`, `−`, numeric px, `+`; 320–2400, step 40), `utf-8[unix]` on `--color-iron`, and scroll position (`Top` / `N%` / `Bot` / `All`) on green.
- Zoom and width persist in `localStorage` (`zoom`, `ancho-notas`, `ancho-exámenes`).

### Keys (htop function-key buttons)
Buttons are `<kbd>` + label pairs: the key on `--color-void`, the label filled with `--ansi-cyan`, or with accent and bold for the primary action. There is no radius. The key label is a real shortcut: `⏎` triggers the primary key, `Esc` goes back.

### Exam
- Question number `[01]` in orange, then the statement.
- Options render as `( )` / `(•)` text: the native radio is visually hidden but stays focusable. The selected option label turns bold paper.
- Grading shows an htop meter, `Score[|||||||     ]70%`, 40 cells, green at 70% or more and red below. Each option then gets `✓` (green), `✕` + strikethrough (red), or `·` (grey). Explanations are prefixed `//`.

### Note document
- Lists: `- ` markers for `ul` (`· ` nested), decimals for `ol`, markers in orange. Bold is paper, italic is yellow.
- The block selector in the waybar always reflects the block under the caret: `¶ párrafo`, `# … ###### título N`, `- lista`, `1. lista numerada`. Picking a value converts the current line in place. From inside a list item, picking a paragraph or heading lifts that line out and splits the list around it. Picking the other list type converts the whole list.
- Typed shortcuts at the start of a line: `/h1`…`/h6`, `/p`, `/lista`, `/ol`, `- `, `* `, `1. `.
- Marks: background, underline or strikethrough in the chosen swatch color. A comment adds a `°` in accent.
- Margin cards: flat `--color-graphite`, 2px left border in the card's own color, 55% opacity until hovered.
- Floating menus, tooltips and reference previews: `--color-void` with a 1px `--color-slate` border, no radius.

## Shape and depth

- Radius: 0 for content (cards, menus, keys, tables); 8px for waybar modules; full pills only for workspaces and color swatches.
- No shadows anywhere. Depth is the step between `void`, `carbon` and `graphite`.
- Borders are 1px hairlines. Dashed only between exam questions.

## Do

- Read colors through tokens only. A hex in a component rule breaks every theme but one.
- Say state with ANSI color and a glyph together (`✓`/`✕`, `NORMAL`/`INSERT`), so e-ink, where hues are grey, still reads.
- Keep headings mono and near body size. Tell levels apart by color and counter.
- Put navigation and tools in the waybar, and view and state controls in the statusline.
- Label buttons like terminal keys, and make the shortcut real.

## Don't

- Don't add shadows, gradients, or large type.
- Don't add radius to content surfaces.
- Don't make the panel its own scroll container.
- Don't store theme-dependent colors in the `.md`.
- Don't use accent fills for anything but the current selection or the primary action.

## Files

| File | Owns |
|---|---|
| `estilo.css` | Tokens, the six theme blocks, and shared components (waybar, explorer, tables, statusline, keys, viz) |
| `tema.js` | Theme list, persistence, `selectorTema()` markup, `elegirTema()` |
| `shell.js` | `montarShell(page)` injects waybar, explorer, panel and statusline; runs the clock, scroll position, zoom and width. Returns `{ app, arbol, herramientas, ruta, modo }` |
| `notas.html` | Editor-specific styles and logic: tools, tree index, document |
| `examen.html` | Exam styles and logic: tree of exams, questions, meter |
| `viz.js` | Mermaid and KaTeX; the Mermaid theme is built from the ramp tokens |
