# Working on Engineeringification

Instructions for any AI assistant (Claude, ChatGPT, Gemini, Qwen, Copilot or another) and for people. Follow them when adding, updating or removing a tool.

This repository is the public site **Engineeringification**: https://david-i-schwartz.github.io/engineeringification/
It holds the public tools, demos and project pages from the Engineeringification work on digital-engineering education (the NSF proposal and related papers). Each tool is a single-file HTML app with its own web address, so it opens on any phone, tablet or computer and can be added to the Home Screen. GitHub Pages serves the `main` branch as it is.

It works the same way as the owner's other site, Web & Mobile Apps (`david-i-schwartz/web-mobile-apps`), and uses the same build tool and house rules.

## Layout

- `src/` holds the published copy of each tool: one HTML file per tool. The master copies live in the owner's RIT Google Drive, under `Claude Apps`.
- `site.json` lists the tools: which file, which folder, and the name and colour for tools that don't carry a spec. Its top part holds the site's title, tagline and address.
- `tools/` is the build tool, from HTML App Generator's kit. It needs Node 18 or later and nothing to install. Keep it the same as `tools/` in `web-mobile-apps`.
- `tests/site.py` checks a built site (Python with Playwright and Chromium).
- The tool folders (such as `mechanics-lab/`), `index.html` (the front page) and `README.md` are **built**. Never edit them by hand: every build rewrites them.
- `HOUSE-RULES.md` lists the rules every tool follows. It's the same file as in `web-mobile-apps`. Read it.
- `LICENSE` is GPL-3.0. Don't change it.

## Public only

This site is public, and so is this repository. Only finished, shareable material goes here: tools, demos, project pages, and papers once they are published or posted. Proposal drafts, budgets, letters of support, reviews and reviewer comments, unpublished data, and anything about people in a study stay on the owner's RIT Drive. If you aren't sure something may be public, ask the owner first.

## Add a tool

1. **Get the tool as one HTML file** that follows `HOUSE-RULES.md`: one file, no outside code, fonts or pictures, no network calls (apart from an optional AI helper the person sets up, as rule 1 allows), and it works in a browser by itself. Open it in a browser and check that the console shows no errors.
2. **Choose a folder name**: lowercase letters, digits and hyphens, for example `mechanics-lab`. This becomes the web address `.../engineeringification/mechanics-lab/`.
3. **Save the file** as `src/<folder>.html`.
4. **Add it to `site.json`**, inside `"apps"`:
   ```json
   {"file": "src/mechanics-lab.html", "folder": "mechanics-lab", "code": "MOL", "name": "Mechanics Overlay Lab",
    "tagline": "One plain sentence about what it does.", "accent": "#B4532A"}
   ```
   - `code`: 2 to 6 capital letters or digits. It's drawn as beads on the Home Screen icon.
   - `accent`: the tool's main colour. If you leave it out, the build uses the page's `--accent` colour, or teal.
5. **Build**, from the repository's top folder:
   ```
   node tools/cli.js site site.json .
   ```
6. **Check it.** Run `python3 tests/site.py .`. It must end with "All checks passed." Without Playwright, serve the folder (`python3 -m http.server 8000`) and open `http://localhost:8000/<folder>/` at a phone size (390 px wide) and a desktop size, with no console errors.
7. **Commit and push to `main`**: the `src/` file, `site.json`, the new folder, `index.html` and `README.md`. Use a short message, such as "Add MOL: Mechanics Overlay Lab". The site updates in a minute or two.
8. **Tell the owner** the new address. Remind them that the master copy belongs in RIT Drive, in `Claude Apps / <tool's folder>`, and that its row in the Apps Registry should name this site.

## Update a tool

Replace `src/<folder>.html` with the new version. Then build, check, commit and push, as in steps 5 to 7.

## Settings files next to a tool

Most tool folders hold only what the build makes. The exception is `mechanics-lab/ai-config.json`, the settings file for Mechanics Overlay Lab's optional AI tutor (house rule 1). It's kept by hand: the build doesn't touch it. Keep `baseUrl` empty, and never put an API key in it.

## Keep src/, tools/ and the site in step

The built folders must always be exactly what `node tools/cli.js site site.json .` makes from `src/`, `site.json` and `tools/`. After building, run `git status`: it should list only the files you meant to change.

## Remove a tool

Delete its entry in `site.json`, its `src/` file and its built folder. Then build, check, commit and push.

## Don't

- Don't edit built files (`index.html`, `README.md`, the tool folders). Change `src/` or `site.json`, then build.
- Don't commit anything from the "Public only" list above, or notes, plans, personal data or passwords.
- Don't publish anything the owner marks private, confidential or under a non-disclosure agreement, and don't mention it here either.
- Don't add libraries, trackers, analytics or anything that loads from another site.
- Don't remove `tools/` or `LICENSE`.

## If you can't push to GitHub

Prepare the HTML file, check it against `HOUSE-RULES.md`, and give it to the owner with the `site.json` entry from step 4.
