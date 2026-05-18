---
name: obsidian-resume
description: >
  Use this skill whenever the user wants to generate a resume, CV, or job application
  materials from their Obsidian notes. Triggers on: "generate resume from Obsidian",
  "make my resume from my notes", "build CV from vault", "create Harvard resume",
  "find jobs matching my resume", "export resume as LaTeX", "resume from markdown notes".
  Also trigger when the user pastes Obsidian markdown and asks for a resume, cover letter,
  or job search. This skill reads exported vault JSON (from export_vault.py), generates
  a Harvard OCS-style LaTeX resume, and runs a live job search based on the user's profile.
---

# Obsidian → Harvard Resume + Job Search Skill

## Overview

This skill does three things in sequence:

1. **Parse** exported Obsidian notes (`obsidian_export.json`) into a structured profile
2. **Generate** a Harvard OCS-style LaTeX resume (compiles to PDF with `pdflatex`)
3. **Search** live job listings that match the user's skills and experience

---

## Step 0 — Check for export file

Before anything else, ask the user:

> "Have you run `export_vault.py` yet? If yes, paste the contents of `obsidian_export.json` here. If not, I can also work directly from pasted markdown notes."

**If they have the JSON:** parse it using the schema in `references/export_schema.md`.  
**If they paste raw markdown:** extract profile data directly — see *Parsing Rules* below.

---

## Step 1 — Parse Obsidian notes into a profile

Build a structured profile object with these fields:

```
profile:
  name: string
  email: string
  phone: string
  location: string
  linkedin: string (optional)
  github: string (optional)
  website: string (optional)
  summary: string (2–3 sentences, optional)

  education:
    - degree: string
      school: string
      location: string
      dates: string          # e.g. "Sep 2016 – Jun 2020"
      gpa: string (optional)
      honors: string (optional)
      relevant_courses: [string] (optional)

  experience:
    - title: string
      company: string
      location: string
      dates: string
      bullets: [string]      # strong action verbs, quantified impact

  projects:
    - name: string
      tech: string           # comma-separated stack
      dates: string (optional)
      bullets: [string]

  skills:
    technical: [string]
    languages: [string]
    tools: [string]
    soft: [string] (optional)

  awards: [string] (optional)
  publications: [string] (optional)
  volunteer: [string] (optional)
```

### Parsing rules

- Obsidian frontmatter keys (`title:`, `company:`, `dates:`, `tags:`) map directly to profile fields
- Headings (`## Experience`, `## Skills`) signal sections
- Bullet points (`-`) under a job heading become `bullets[]`
- Dataview fields (`company:: Acme Corp`) are treated like frontmatter
- Tags `#career`, `#resume`, `#job` mark notes as relevant
- If a field is missing, leave it out — do NOT invent data
- Dates: preserve whatever format the user wrote; do not reformat

---

## Step 2 — Generate Harvard OCS LaTeX resume

Read the full template in `references/harvard_template.md` before generating.

### Harvard OCS rules (strict)

| Rule | Detail |
|------|--------|
| Font | 10–12pt, Times New Roman or Latin Modern |
| Margins | 0.5–1 inch all sides |
| Section headers | ALL CAPS, bold, followed by a full-width horizontal rule |
| Name | Large (16–18pt), bold, centered at top |
| Contact line | Single line, centered, below name |
| Dates | Right-aligned on same line as job title/company |
| Bullets | Start with strong past-tense action verb; quantify impact where possible |
| Length | 1 page for <10 years experience; 2 pages max |
| Order | Education → Experience → Projects → Skills → Awards |
| No photos | No headshots or graphics |
| No colors | Pure black and white (use `\color{black}` everywhere) |

### LaTeX output format

Output the complete `.tex` file — do not truncate. Structure:

```latex
\documentclass[10pt, letterpaper]{article}
% ... preamble (see references/harvard_template.md for full preamble)

\begin{document}

% ── HEADER ──────────────────────────────────────────────────
\begin{center}
  {\LARGE\textbf{FULL NAME}} \\[4pt]
  \small email@example.com \; $\cdot$ \; +1 (555) 000-0000 \; $\cdot$ \; City, Country \\
  \small \href{https://linkedin.com/in/handle}{linkedin.com/in/handle} \; $\cdot$ \; \href{https://github.com/handle}{github.com/handle}
\end{center}

\vspace{-6pt}

% ── EDUCATION ───────────────────────────────────────────────
\section*{EDUCATION}
\hrule
\vspace{4pt}

\noindent\textbf{University Name} \hfill City, Country \\
\textit{Degree, Major} \hfill \textit{Sep 20XX -- Jun 20XX} \\
GPA: X.X/4.0 \; | \; Honors: Dean's List

\vspace{6pt}

% ── EXPERIENCE ──────────────────────────────────────────────
\section*{EXPERIENCE}
\hrule
\vspace{4pt}

\noindent\textbf{Company Name} \hfill City, Country \\
\textit{Job Title} \hfill \textit{Jan 20XX -- Dec 20XX}
\begin{itemize}[leftmargin=1.5em, topsep=2pt, itemsep=0pt]
  \item Accomplished [X] by doing [Y], resulting in [Z\%] improvement
  \item Led team of N engineers to deliver feature used by X users
\end{itemize}

\vspace{6pt}

% ── PROJECTS ────────────────────────────────────────────────
\section*{PROJECTS}
\hrule
\vspace{4pt}

\noindent\textbf{Project Name} \textit{| Tech Stack} \hfill \textit{Month 20XX}
\begin{itemize}[leftmargin=1.5em, topsep=2pt, itemsep=0pt]
  \item Built [X] using [Y] that achieved [Z]
\end{itemize}

\vspace{6pt}

% ── SKILLS ──────────────────────────────────────────────────
\section*{SKILLS}
\hrule
\vspace{4pt}

\noindent\textbf{Languages:} Python, TypeScript, Go \\
\noindent\textbf{Frameworks:} React, FastAPI, Node.js \\
\noindent\textbf{Tools:} Docker, GitHub Actions, AWS, PostgreSQL

\end{document}
```

### LaTeX special characters — escape these always

| Character | Escaped |
|-----------|---------|
| `&` | `\&` |
| `%` | `\%` |
| `$` | `\$` |
| `#` | `\#` |
| `_` | `\_` |
| `{` `}` | `\{` `\}` |
| `~` | `\textasciitilde{}` |
| `^` | `\textasciicircum{}` |
| `\` | `\textbackslash{}` |

Vietnamese and accented characters work natively with `\usepackage[T1]{fontenc}` + `\usepackage[utf8]{inputenc}` — include both in preamble.

### Bullet writing rules

Rewrite the user's raw notes into resume bullets:
- Start with a past-tense action verb (Built, Led, Designed, Reduced, Launched, Automated...)
- Include a metric whenever the notes hint at one (users, %, time saved, $ value, team size)
- Keep each bullet to 1 line (≤90 chars) where possible
- Do NOT invent metrics — if there are none, write a strong qualitative bullet

---

## Step 3 — Live job search

After generating the resume, extract a search profile:

```
search_profile:
  top_skills: [3–5 most prominent technical skills]
  roles: [2–3 job titles that fit the experience level]
  location: [from profile, default "Ho Chi Minh City" or "Remote"]
  years_experience: [estimate from dates]
  seniority: [Junior / Mid / Senior / Lead]
```

Then use **web search** to find live job listings. Run these searches:

1. `"{role}" "{top_skill}" jobs {location} 2025`
2. `"{role}" remote Vietnam 2025 site:linkedin.com OR site:vietnamworks.com OR site:topcv.vn`
3. `"{role}" "{top_skill}" "{top_skill_2}" job opening`

For each search, extract up to 3 real listings with:
- Job title
- Company
- Location / Remote status
- URL to apply
- Why it matches (1 sentence referencing specific skills from the resume)

Present results as a table:

| Role | Company | Location | Match reason | Link |
|------|---------|----------|--------------|------|
| ... | ... | ... | ... | [Apply](...) |

Then offer to write a tailored cover letter for any listing.

---

## Step 4 — Cover letter (on request)

When the user picks a job, generate a cover letter:

- **Format:** Plain text, 3 paragraphs, under 280 words
- **Para 1:** Why this specific company/role (reference something real about the company)
- **Para 2:** 2 strongest achievements from the resume that match the job
- **Para 3:** Brief close + call to action
- **Tone:** Confident, direct, not generic — avoid phrases like "I am writing to express my interest"

---

## Output checklist

Before presenting the LaTeX to the user, verify:

- [ ] All special characters are escaped
- [ ] `inputenc` and `fontenc` packages included (for non-ASCII names)
- [ ] Every `\begin{}` has a matching `\end{}`
- [ ] Dates are right-aligned using `\hfill`
- [ ] Section headers use `\section*{}` (no numbering) + `\hrule`
- [ ] No invented data — only what came from the notes
- [ ] File compiles with `pdflatex resume.tex` (mentally trace through)

---

## Files in this skill

| File | Purpose |
|------|---------|
| `SKILL.md` | This file — main instructions |
| `scripts/export_vault.py` | Run locally to export Obsidian vault → JSON |
| `references/harvard_template.md` | Full LaTeX preamble + section examples |
| `references/export_schema.md` | JSON schema for `obsidian_export.json` |

---

## Quick reference — how to use this skill

1. Run `python export_vault.py --vault ~/path/to/vault` on your computer
2. Paste the output JSON into Claude
3. Claude generates your Harvard LaTeX resume
4. Save the `.tex` file and compile: `pdflatex resume.tex`
5. Claude searches live jobs matching your profile
6. Pick a job → Claude writes a tailored cover letter
