---
description: Search live job listings that match the user's resume / Obsidian profile
argument-hint: "[path to resume.tex, obsidian_export.json, or pasted profile]"
---

# /find-jobs

Search live job listings that match the user's skills and experience.

**Plugin root:** `${CLAUDE_PLUGIN_ROOT}`
**Skill source of truth:** `${CLAUDE_PLUGIN_ROOT}/skills/obsidian-resume/`

Follow these steps in order. Do not skip steps.

---

## Step 1 — Locate the input

The user may have passed input as `$ARGUMENTS`. Resolve it like this:

1. **If `$ARGUMENTS` is a `.tex` file** → read it; extract skills/roles/location from the LaTeX content.
2. **If `$ARGUMENTS` is a `.json` file** → read it as the Obsidian export.
3. **If `$ARGUMENTS` is a `.md` file** → read it as raw notes.
4. **If `$ARGUMENTS` is empty** → ask:
   > "Give me a file path to your resume (`resume.tex`), your `obsidian_export.json`, or paste your profile here. If you haven't generated a resume yet, run `/generate-resume` first."

Do not proceed without content.

---

## Step 2 — Read the workflow reference

Read `${CLAUDE_PLUGIN_ROOT}/skills/obsidian-resume/SKILL.md` Step 3 in full. That section is the authoritative spec for the search.

---

## Step 3 — Build the search profile

Extract this from the input:

```
search_profile:
  top_skills: [3–5 most prominent technical skills]
  roles: [2–3 job titles that fit the experience level]
  location: [from profile; default to user's stated location or "Remote"]
  years_experience: [estimate from dates]
  seniority: [Junior / Mid / Senior / Lead]
```

Show the search profile to the user before searching so they can correct it:
> "I'll search for these roles in this location based on your skills. Anything I should adjust?"

Wait for confirmation or edits.

---

## Step 4 — Run the searches

Use the **WebSearch tool**. Run these three queries (substituting actual values, and using the *current* year from the environment, not a hardcoded one):

1. `"{role}" "{top_skill}" jobs {location} {current_year}`
2. `"{role}" remote {country} {current_year} site:linkedin.com OR site:<local-board>`
3. `"{role}" "{top_skill}" "{top_skill_2}" job opening`

Adapt query #2 to the user's region — match the local job-board landscape:
- Vietnam: `vietnamworks.com`, `topcv.vn`, `itviec.com`
- US: `indeed.com`, `glassdoor.com`
- Australia: `seek.com.au`
- UK: `reed.co.uk`
- Singapore: `mycareersfuture.gov.sg`
- Default global: `linkedin.com`, `indeed.com`

---

## Step 5 — Present results

For each search, extract up to 3 real listings. Filter out:
- Expired postings
- Listings clearly mismatched on seniority
- Listings that require skills the user doesn't have at all (a mild gap is OK and worth flagging)

Present results as a single combined table:

| Role | Company | Location | Match reason | Link |
|------|---------|----------|--------------|------|
| ... | ... | ... | One sentence referencing specific skills from the resume | [Apply](url) |

**Match reason** must reference specific skills or experience from the resume — not generic phrases.

If a search returns no usable results, say so honestly. Do not fabricate listings.

---

## Step 6 — Offer cover letter

After the table, offer:
> "Want me to write a tailored cover letter for any of these? Tell me which row."

When the user picks one, generate per `SKILL.md` Step 4:
- Plain text, 3 paragraphs, under 280 words
- Para 1: why this specific company/role (something real about the company)
- Para 2: 2 strongest achievements from the resume that match the job
- Para 3: brief close + call to action
- Confident, direct tone — no "I am writing to express my interest"

---

## Important

- **Never fabricate job listings.** If a search yields nothing usable, report that and try a different query.
- Verify links look like real job posting URLs before presenting them.
- Use the actual current year from the environment in queries, not stale dates.
- If WebSearch is unavailable, tell the user and stop — do not invent results.
