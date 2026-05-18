---
description: Generate a Harvard OCS-style LaTeX resume from Obsidian vault notes
argument-hint: "[path to obsidian_export.json or resume markdown]"
---

# /generate-resume

Generate a Harvard OCS-style LaTeX resume from the user's Obsidian notes.

**Plugin root:** `${CLAUDE_PLUGIN_ROOT}`
**Skill source of truth:** `${CLAUDE_PLUGIN_ROOT}/skills/obsidian-resume/`

Follow these steps in order. Do not skip steps.

---

## Step 1 — Locate the input

The user may have passed input as `$ARGUMENTS`. Resolve it like this:

1. **If `$ARGUMENTS` is a directory** → it's an Obsidian vault. Run the export script on it (see Step 1a below). **This is the recommended path.**
2. **If `$ARGUMENTS` is a `.json` file** → read it with the Read tool. This is a pre-exported `obsidian_export.json`.
3. **If `$ARGUMENTS` is a `.md` file** → read it. Treat as raw resume notes.
4. **If `$ARGUMENTS` is empty** → ask the user:
   > "Give me a path to your Obsidian vault folder, a pre-exported `obsidian_export.json`, or paste markdown notes here."

Use Bash `test -d "$ARGUMENTS"` to distinguish a directory from a file.

Do not proceed until you have actual content.

---

## Step 1a — Run the export script (when input is a folder)

When the user passes a vault path, invoke the bundled Python exporter via the Bash tool — do not reimplement the parsing inline.

```bash
OUT="$(mktemp -t obsidian_export.XXXXXX.json)"
python3 "${CLAUDE_PLUGIN_ROOT}/skills/obsidian-resume/scripts/export_vault.py" \
  --vault "$ARGUMENTS" \
  --out "$OUT"
echo "$OUT"
```

Then read the JSON file at the path printed by `echo`. The script handles:

- Walking the vault and skipping `.obsidian/`, `.trash/`, and other dot-directories
- Filtering for career-tagged notes (`#career`, `#resume`, `#job`, `#experience`, etc.)
  or career-named folders (`Career`, `Job`, `Resume`, `CV`, `Work`, `Experience`, `Portfolio`, ...)
- Parsing YAML frontmatter, inline tags, and Dataview `key:: value` fields
- Producing the JSON schema documented in `references/export_schema.md`

**If the script fails:**

- `python3: command not found` → tell the user they need Python 3 installed and stop.
- `Vault not found` → the path was wrong; ask the user for the correct path.
- Anything else → show the user the error and stop.

**If the script returns zero notes:**

Re-run with `--all` to include every `.md` file, or ask the user which folder/tag to scope to:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/obsidian-resume/scripts/export_vault.py" \
  --vault "$ARGUMENTS" --all --out "$OUT"
```

**Once you have the JSON, read it with the Read tool and proceed to Step 3.**

---

## Step 2 — Read the references

Before generating LaTeX, read these in full:

1. `${CLAUDE_PLUGIN_ROOT}/skills/obsidian-resume/SKILL.md` — full workflow
2. `${CLAUDE_PLUGIN_ROOT}/skills/obsidian-resume/references/harvard_template.md` — LaTeX preamble + section examples
3. `${CLAUDE_PLUGIN_ROOT}/skills/obsidian-resume/references/export_schema.md` — JSON schema (only if working from JSON)

These files are the authoritative spec. The rules in them override anything else.

---

## Step 3 — Parse the input into a profile

Build the structured profile object defined in `SKILL.md` Step 1.

Rules:
- Frontmatter keys (`title:`, `company:`, `dates:`, `tags:`) map directly to profile fields
- `## Experience`, `## Skills` headings signal sections
- Bullets under a job heading become `bullets[]`
- Dataview fields (`company:: Acme`) are treated like frontmatter
- Tags `#career`, `#resume`, `#job` mark notes as relevant
- **If a field is missing, leave it out. Do NOT invent data.**
- Preserve the user's date format — do not reformat

---

## Step 4 — Generate the LaTeX resume

Apply every rule from `references/harvard_template.md`:

- Use the full preamble exactly as written there
- Section order: Education → Experience → Projects → Skills → Awards
- ALL CAPS section headers with `\hrule`
- Dates right-aligned with `\hfill`
- Bullets: past-tense action verbs, quantified impact where the notes support it
- Escape LaTeX specials: `& % $ # _ { } ~ ^ \`
- Include `\usepackage[utf8]{inputenc}` and `\usepackage[T1]{fontenc}` for accented names
- 1 page target (2 max for 10+ years experience)

Run the **output checklist** from `SKILL.md`:

- [ ] All special characters escaped
- [ ] `inputenc` and `fontenc` included
- [ ] Every `\begin{}` matches an `\end{}`
- [ ] Dates right-aligned with `\hfill`
- [ ] Section headers use `\section*{}` + `\hrule`
- [ ] No invented data
- [ ] File would compile with `pdflatex` (mentally trace)

---

## Step 5 — Save the output

Ask the user where to save:
> "Where should I save the `.tex` file? (default: `./resume.tex`)"

Write the complete `.tex` to that path with the Write tool. Then print compile instructions:

```bash
pdflatex resume.tex
pdflatex resume.tex   # run twice for correct spacing
```

If `pdflatex` isn't installed, point to:
- macOS:   `brew install --cask mactex`
- Ubuntu:  `sudo apt install texlive-full`
- Windows: MiKTeX from miktex.org

---

## Step 6 — Offer the next step

After saving, offer:
> "Resume saved. Want me to find live job listings that match this profile? Run `/find-jobs` with the same input."

---

## Important

- **Never invent achievements, metrics, dates, employers, or education.** Only use what's in the notes.
- If the notes are sparse, write strong qualitative bullets — do not pad with fake metrics.
- Vietnamese / accented characters work natively with `inputenc` + `fontenc`. Do not transliterate names.
