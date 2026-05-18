# Harvard OCS Resume — Full LaTeX Reference

This file contains the complete preamble and section-by-section examples.
Read this entire file before generating any LaTeX output.

---

## Full preamble (copy exactly)

```latex
\documentclass[10pt, letterpaper]{article}

% --- Encoding (required for Vietnamese / accented names) ---
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}

% --- Font: Latin Modern (closest free match to Times) ---
\usepackage{lmodern}

% --- Margins ---
\usepackage[
  top=0.6in, bottom=0.6in,
  left=0.75in, right=0.75in
]{geometry}

% --- Hyperlinks ---
\usepackage[
  colorlinks=false,
  pdfborder={0 0 0}
]{hyperref}

% --- List formatting ---
\usepackage{enumitem}
\setlist[itemize]{
  leftmargin=1.5em,
  topsep=2pt,
  itemsep=0pt,
  parsep=0pt,
  label=\textbullet
}

% --- Suppress page numbers ---
\pagestyle{empty}

% --- Micro-typography ---
\usepackage{microtype}

% --- No paragraph indent ---
\setlength{\parindent}{0pt}

% --- Section style: ALL CAPS + bold + hrule below ---
\usepackage{titlesec}
\titleformat{\section}
  {\normalsize\bfseries\uppercase}
  {}{0em}{}
  [\vspace{-6pt}\rule{\textwidth}{0.4pt}]
\titlespacing{\section}{0pt}{10pt}{4pt}
```

---

## Header block

```latex
\begin{document}

\begin{center}
  {\Large\textbf{Nguyen Van An}} \\[3pt]
  \small
  \href{mailto:van.an@email.com}{van.an@email.com} \;$\cdot$\;
  +84 90 123 4567 \;$\cdot$\;
  Ho Chi Minh City, Vietnam \\[1pt]
  \href{https://linkedin.com/in/vanan}{linkedin.com/in/vanan} \;$\cdot$\;
  \href{https://github.com/vanan}{github.com/vanan}
\end{center}

\vspace{2pt}
```

**Rules:**
- Name: `\Large\textbf{}` — never larger than `\LARGE`
- Contact on one line separated by `\;$\cdot$\;`
- If LinkedIn or GitHub is missing, omit the whole line
- Email must be a `\href{mailto:...}{...}` link

---

## Education section

```latex
\section{Education}

\textbf{Ho Chi Minh City University of Technology} \hfill Ho Chi Minh City, Vietnam \\
\textit{Bachelor of Science in Computer Science} \hfill \textit{Sep 2016 -- Jun 2020} \\
GPA: 3.6/4.0 \;$|$\; Dean's List (4 semesters)

\vspace{4pt}

% If there are relevant courses:
\textit{Relevant coursework:} Data Structures, Algorithms, Operating Systems, Machine Learning
```

**Rules:**
- School name bold, location right-aligned with `\hfill`
- Degree italic, dates italic + right-aligned
- GPA only if ≥ 3.0 (or equivalent scale)
- Multiple schools: separate with `\vspace{4pt}`

---

## Experience section

```latex
\section{Experience}

\textbf{Startup XYZ} \hfill Ho Chi Minh City, Vietnam \\
\textit{Senior Full Stack Engineer} \hfill \textit{Jan 2022 -- Dec 2024}
\begin{itemize}
  \item Rebuilt monolithic platform into microservices, reducing API latency by 60\% (p99)
  \item Led team of 5 engineers across 3 timezones to ship 3 major features for 50k+ MAU
  \item Introduced CI/CD pipeline with GitHub Actions, cutting deploy time from 2h to 8min
\end{itemize}

\vspace{4pt}

\textbf{Agency ABC} \hfill Ho Chi Minh City, Vietnam \\
\textit{Full Stack Developer} \hfill \textit{Jun 2020 -- Dec 2021}
\begin{itemize}
  \item Delivered 12+ client web apps (SaaS, e-commerce, internal tools) on time and budget
  \item Built reusable React component library adopted across 8 projects, saving 30\% dev time
\end{itemize}
```

**Rules:**
- Company bold, location right-aligned
- Title italic, dates italic + right-aligned — both on second line
- 3–5 bullets per role
- Every bullet starts with a strong past-tense verb
- Escape `%` as `\%`
- Separate roles with `\vspace{4pt}`

---

## Projects section

```latex
\section{Projects}

\textbf{Budgeting App} \textit{$|$ React Native, Supabase, TypeScript} \hfill \textit{2023}
\begin{itemize}
  \item Multi-currency tracking app with 1,200+ Google Play downloads and 4.6-star rating
  \item Implemented real-time sync and offline-first architecture using Supabase Realtime
\end{itemize}

\vspace{4pt}

\textbf{react-csv-toolkit} \textit{$|$ TypeScript, Zod} \hfill \textit{2022 -- Present}
\begin{itemize}
  \item Open-source npm package with 800+ weekly downloads; handles CSV import with schema validation
\end{itemize}
```

**Rules:**
- Project name bold, tech stack italic after `\textit{$|$}`
- Date right-aligned with `\hfill`
- 1–2 bullets for personal projects, 2–3 for major ones
- Include links as `\href{url}{Project Name}` in the name if public

---

## Skills section

```latex
\section{Skills}

\textbf{Languages:} Python, TypeScript, Go, SQL \\
\textbf{Frameworks \& Libraries:} React, Next.js, FastAPI, Node.js, Tailwind CSS \\
\textbf{Tools \& Platforms:} Docker, GitHub Actions, AWS (EC2, S3, RDS), PostgreSQL, Redis \\
\textbf{Languages (spoken):} Vietnamese (native), English (professional)
```

**Rules:**
- Category bold, colon, then comma-separated list
- Each category on its own line with `\\`
- Order: Languages → Frameworks → Tools → Spoken languages
- No more than 4–5 categories
- Do not list soft skills here — they belong in bullets

---

## Awards / Certifications section (optional)

```latex
\section{Awards \& Certifications}

AWS Certified Solutions Architect -- Associate \hfill \textit{2023} \\
1st Place, Vietnam Hackathon 2022 \hfill \textit{2022} \\
Dean's List, HCMUT (4 semesters) \hfill \textit{2016--2020}
```

---

## Closing tag

Always end with:

```latex
\end{document}
```

---

## Compile instructions (tell the user)

```bash
# Install TeX Live (one-time)
# macOS:   brew install --cask mactex
# Ubuntu:  sudo apt install texlive-full
# Windows: install MiKTeX from miktex.org

# Compile (run twice for correct spacing)
pdflatex resume.tex
pdflatex resume.tex

# Output: resume.pdf
```

---

## Common errors and fixes

| Error | Fix |
|-------|-----|
| `! Missing $ inserted` | An `&`, `%`, `_`, or `^` is not escaped |
| `! Undefined control sequence` | Typo in a command name |
| `Package inputenc Error` | Add `\usepackage[utf8]{inputenc}` to preamble |
| Dates not right-aligned | Use `\hfill` between name and date on same line |
| Section has number prefix | Use `\section*{}` or configure titlesec to suppress |
| Text overflows margin | Shorten the bullet; add `\sloppy` before problem paragraph |
