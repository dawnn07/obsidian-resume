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

1. **If `$ARGUMENTS` is a directory** → it's an Obsidian vault. Discover career notes inline (see Step 1a below). **This is the recommended path — no Python script needed.**
2. **If `$ARGUMENTS` is a `.json` file** → read it with the Read tool. This is a pre-exported `obsidian_export.json`.
3. **If `$ARGUMENTS` is a `.md` file** → read it. Treat as raw resume notes.
4. **If `$ARGUMENTS` is empty** → ask the user:
   > "Give me a path to your Obsidian vault folder, a pre-exported `obsidian_export.json`, or paste markdown notes here."

Use Bash `test -d "$ARGUMENTS"` to distinguish a directory from a file.

Do not proceed until you have actual content.

---

## Step 1a — Vault discovery (when input is a folder)

When the user passes a vault path, walk it yourself with these tools — do not ask them to run the Python export script.

**Discovery procedure:**

1. **Find candidate files:** Use Glob with pattern `**/*.md` inside the vault path. Exclude anything under `.obsidian/`, `.trash/`, or any directory starting with `.`.

2. **Filter by relevance.** Keep a note if ANY of these is true:
   - It lives inside a folder named (case-insensitive): `Career`, `Job`, `Resume`, `CV`, `Work`, `Experience`, `Portfolio`, `About Me`, or `Nghề nghiệp`
   - It contains one of these tags (frontmatter `tags:` array OR inline `#tag`): `career`, `resume`, `job`, `work`, `experience`, `skills`, `education`, `projects`, `cv`, `portfolio`

   Use Grep with pattern `#(career|resume|job|work|experience|skills|education|projects|cv|portfolio)\b` over the vault to find tagged notes fast, then merge with the folder-based matches.

3. **Cap the read set.** If filtering yields more than 50 files, ask the user which subfolders to include before reading everything — context budget matters.

4. **Read the surviving files** with the Read tool, then parse each into the schema below.

**Parsing each file** (same rules as `scripts/export_vault.py` and `references/export_schema.md`):

- Strip the YAML frontmatter from the top (delimited by `---` ... `---`) and parse it as key-value pairs. Lists in `[a, b]` form become arrays.
- Collect inline tags via `#tagname` regex from the body.
- Collect Dataview fields: lines matching `^([A-Za-z_][A-Za-z0-9_ ]*)::\s*(.+)$`.
- The remaining markdown is the note body. Headings, bullet lists, and prose are all consumed in Step 3.

**Large-vault fallback.** If the user explicitly says their vault is huge or context is tight, suggest the Python script as an optional pre-filter:

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/obsidian-resume/scripts/export_vault.py --vault <path>
```

But this is a fallback, not the default flow.

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
