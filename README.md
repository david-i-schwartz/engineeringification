# engineeringification
Tools, demos and project pages from the Engineeringification work on digital-engineering education.

Site: https://david-i-schwartz.github.io/engineeringification/

- [`mechanics-lab/`](https://david-i-schwartz.github.io/engineeringification/mechanics-lab/): MOL, Mechanics Overlay Lab

## How it works

- `src/` holds the published copy of each tool, one HTML file each. `site.json` lists them.
- `node tools/cli.js site site.json .` builds a folder for each tool: the tool (`index.html`), Home Screen icons, `manifest.webmanifest`, and `sw.js`, an offline helper. It also builds the front page and this README.
- To add, update or remove a tool, follow `AGENTS.md`. It's written for any AI assistant or person. The rules every tool follows are in `HOUSE-RULES.md`.

## License

The code in this repository is licensed under the GNU General Public License v3.0 (see `LICENSE`). Anything the tools credit to others keeps its own terms.
