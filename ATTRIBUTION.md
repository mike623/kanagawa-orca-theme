# Sources and adaptation

The following source files and licenses were inspected for this port. Revisions
are pinned for reproducibility; upstream branches may change independently.

| Source | Revision | Used for | License |
| --- | --- | --- | --- |
| [Official Orca Midnight](https://github.com/stablyai/orca-plugins/tree/07590d2c7bdc8c6c9299123106b9e0525656a411/plugins/midnight-theme) | `07590d2c7bdc8c6c9299123106b9e0525656a411` | `orca-plugin.json`, `themes/midnight.json`: data-only manifest and app/editor structure | [MIT, Lovecast Inc.](licenses/orca-midnight-MIT.txt) |
| [kanagawa.nvim](https://github.com/rebelot/kanagawa.nvim/tree/bb85e4bfc8d89b0e62c8fa53ccdd13d12e2f77b3) | `bb85e4bfc8d89b0e62c8fa53ccdd13d12e2f77b3` | `lua/kanagawa/colors.lua`, `lua/kanagawa/themes.lua`: original named palettes, variant roles and terminal colors; `lua/kanagawa/highlights/{syntax,treesitter}.lua`: syntax colors and font styles | [MIT, Tommaso Laurenzi](licenses/kanagawa.nvim-MIT.txt) |
| [Kanagawa VS Code](https://github.com/paccodes/kanagawa-vscode-theme/tree/60f23d7520c80385071b7e47a9f83708e647f1a9) | `60f23d7520c80385071b7e47a9f83708e647f1a9` | `themes/kanagawa-{wave,dragon,lotus}-color-theme.json`: UI mappings and terminal palettes | [MIT, Pierre-Alain Castella](licenses/kanagawa-vscode-MIT.txt) |

The requested [Marketplace listing](https://marketplace.visualstudio.com/items?itemName=metaphore.kanagawa-vscode-color-theme)
links to the `paccodes/kanagawa-vscode-theme` repository. Its README also credits
[the earlier barklan VS Code port](https://github.com/barklan/kanagawa.vscode).
No code or artwork was separately copied from that earlier repository. No
upstream screenshots or Hokusai image assets are included.

## Orca guidance

Followed the official [plugin authoring guide](https://github.com/stablyai/orca/blob/main/docs/reference/plugin-authoring.md),
[theme format](https://github.com/stablyai/orca/blob/main/docs/reference/plugin-themes.md)
and [public token reference](https://github.com/stablyai/orca/blob/main/docs/reference/plugin-theme-tokens.md).
The official [Gruvbox plugin](https://github.com/stablyai/orca-plugins/tree/07590d2c7bdc8c6c9299123106b9e0525656a411/plugins/gruvbox-theme)
provided a supplementary example of separate app and terminal contributions.

The scaffold's plugin ID, version and minimum Orca version are retained. The
placeholder theme is replaced with three named variants. Unlike the historical
Midnight manifest, this manifest omits deprecated `publisher` metadata; Orca
assigns `local` for a development folder. No repository URL is invented.

## Mapping decisions

- App/editor canvas and foreground match each upstream variant. Cards use the
  VS Code activity-bar fill, sidebars use inactive-tab fills, popovers use
  dropdown fills, and selected rows use active-list fills. Blue function/link
  colors supply primary controls and focus rings. Borders use the upstream menu
  separator color. Explicit text/surface pairs preserve readability.
- Wave uses `oldWhite` for secondary UI text; Dragon uses `dragonGray`. Lotus
  uses `lotusInk1` for secondary UI text because the upstream dim color does not
  reach 4.5:1 on its muted fill.
- Syntax rules are generated from kanagawa.nvim's `syn` palette and highlight
  groups (for example italic keywords, bold `Statement`, `special3` returns and
  exceptions), mapped to TextMate scopes and Monaco Monarch tokens. Semantic
  token colors and VS Code-only UI keys are not copied into Orca JSON.
- Lotus syntax substitutions (all from the original named palette):
  `lotusGray3` `#8A8980` → `lotusGray2` `#716E61` (comments);
  `lotusTeal2` `#6693BF` → `lotusBlue4` `#4D699B`;
  `lotusGreen2` `#6E915F` → `lotusGreen` `#6F894E`;
  `lotusYellow3` `#DE9800` → `lotusYellow2` `#836F4A`.
  The originals are below Orca's 3:1 syntax threshold on Lotus's canvas.
- Lotus added/renamed/untracked/copied Git decorations and added diff hue use
  `lotusAqua` `#597B75`; modified decorations use `lotusYellow2` `#836F4A`.
  These remain legible on the darker sidebar, where the original green and
  yellow do not meet Orca's 3:1 Git-decoration threshold.
- All 16 terminal ANSI slots match both upstream sources. Terminal background,
  foreground and selection follow the VS Code port; cursor uses the variant's
  foreground. Neovim's two extra indexed colors are omitted because Orca's
  terminal format exposes the standard 16 slots.
- Selection and diff surface tints use Orca's derived defaults. No background
  images, executable code, extra theme variants or new dependency are needed.
