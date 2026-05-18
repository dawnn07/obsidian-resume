# obsidian-resume

A Claude Code plugin that turns your **Obsidian vault notes** into a polished **Harvard OCS-style LaTeX resume**, then finds **live job listings** that match your profile.

Two slash commands:

- **`/generate-resume`** — parses your exported Obsidian notes and outputs a complete `.tex` file ready to compile with `pdflatex`.
- **`/find-jobs`** — extracts a search profile from your resume and runs live web searches for matching roles (with optional tailored cover letters).

---

## Install

In Claude Code, run:

```
/plugin install dawnn07/obsidian-resume
```

> Replace `dawnn07/obsidian-resume` with your fork if you've forked it.

That's it. Both `/generate-resume` and `/find-jobs` will appear in your slash-command menu.

---

## Quick start

### 1. Generate the resume

Just point `/generate-resume` at your vault folder — no export step needed:

```
/generate-resume ~/path/to/your/ObsidianVault
```

Claude will:

1. Discover career-relevant notes inside the vault (by folder name or by `#career` / `#resume` / `#job` / `#experience` / etc. tags)
2. Parse the notes into a structured profile
3. Generate a complete Harvard OCS LaTeX file
4. Save it to `./resume.tex` (or a path you choose)
5. Print compile instructions

Compile:

```bash
pdflatex resume.tex
pdflatex resume.tex   # run twice for spacing
```

`/generate-resume` also accepts:

- A pre-exported `obsidian_export.json` file (see [optional pre-export](#optional-pre-export-for-huge-vaults) below)
- A single `.md` file with raw notes
- No argument — it'll ask you for a path or pasted content

### 2. Find matching jobs

```
/find-jobs ./resume.tex
```

Claude extracts your top skills, roles, location and seniority, runs three live web searches, and presents a table of real listings with a one-line "why this matches" for each. Pick a row and Claude will write a tailored cover letter.

---

## Optional: pre-export for huge vaults

If your vault has thousands of notes and reading them inline would burn through context, you can pre-filter into a single JSON file using the included script:

```bash
python ~/.claude/plugins/obsidian-resume/skills/obsidian-resume/scripts/export_vault.py \
  --vault ~/path/to/your/ObsidianVault
```

This produces `obsidian_export.json` in the same folder. The script collects notes that:

- Have a tag in `{career, resume, job, work, experience, skills, education, projects, cv}`
- OR live inside a folder named `Career`, `Job`, `Resume`, `CV`, `Work`, `Experience`, or `Portfolio`

Pass `--all` to export every note, or `--tag mytag` to filter by a specific tag. Then run:

```
/generate-resume /absolute/path/to/obsidian_export.json
```

For typical vaults (a few hundred career-tagged notes or fewer), you don't need this step.

---

## How notes get parsed

Any of these patterns in your Obsidian vault are recognized:

**Frontmatter:**

```markdown
---
tags: [career, experience]
company: Startup XYZ
title: Senior Full Stack Engineer
dates: Jan 2022 – Dec 2024
location: Ho Chi Minh City
---

- Rebuilt monolithic platform into microservices, reducing latency 60%
- Led 5-person engineering team
```

**Heading-based sections:**

```markdown
# Experience

## Senior Engineer at Startup XYZ (2022–2024)

- Built APIs used by 50k users
- Led CI/CD migration
```

**Dataview fields:**

```markdown
company:: Startup XYZ
role:: Senior Full Stack Engineer
start:: 2022-01
end:: 2024-12
```

**Free-form prose** also works — the plugin extracts what it can from any markdown.

See [`skills/obsidian-resume/references/export_schema.md`](skills/obsidian-resume/references/export_schema.md) for the full schema.

---

## Resume style

The plugin follows the **Harvard OCS** resume guidelines strictly:

- 10–12pt Latin Modern (Times-equivalent)
- 0.5–0.75in margins
- ALL CAPS section headers with a horizontal rule
- Dates right-aligned with `\hfill`
- Past-tense action verbs, quantified impact
- 1 page (or 2 max for 10+ years of experience)
- Pure black-and-white, no graphics

Full template and rules: [`skills/obsidian-resume/references/harvard_template.md`](skills/obsidian-resume/references/harvard_template.md).

The plugin will **never** invent data — if your notes don't include a metric, you get a strong qualitative bullet instead of a fabricated number.

---

## Requirements

- **Claude Code** (any recent version with `/plugin install` support)
- **Python 3** (for the vault export script)
- **`pdflatex`** (TeX Live, MacTeX, or MiKTeX) to compile the resume PDF

Unicode names work out of the box (Vietnamese, accented Latin, etc.) — the template includes `inputenc` + `fontenc`.

---

## Plugin structure

```
obsidian-resume/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   ├── generate-resume.md       # /generate-resume
│   └── find-jobs.md             # /find-jobs
├── skills/
│   └── obsidian-resume/
│       ├── SKILL.md             # full workflow (also auto-triggered)
│       ├── references/
│       │   ├── harvard_template.md
│       │   └── export_schema.md
│       ├── assets/
│       │   └── harvard_template.tex
│       └── scripts/
│           └── export_vault.py
└── README.md
```

---

## License

MIT
