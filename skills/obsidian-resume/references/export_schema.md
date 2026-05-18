# Export Schema — `obsidian_export.json`

This file documents the JSON structure produced by `scripts/export_vault.py`.
Claude reads this to understand the input format before parsing.

---

## Top-level structure

```json
{
  "exported_at": "2025-05-17T10:30:00",
  "vault_name": "My Vault",
  "notes": [
    {
      "filename": "Career - Skills.md",
      "path": "Career/Career - Skills.md",
      "tags": ["career", "skills"],
      "frontmatter": {
        "title": "My Skills",
        "updated": "2025-04-01"
      },
      "content": "# My Skills\n\n## Technical\n- Python, TypeScript..."
    }
  ]
}
```

---

## Fields

| Field | Type | Description |
|-------|------|-------------|
| `exported_at` | ISO datetime string | When the export ran |
| `vault_name` | string | Name of the Obsidian vault folder |
| `notes` | array | All collected notes |
| `notes[].filename` | string | Bare filename with `.md` |
| `notes[].path` | string | Relative path inside vault |
| `notes[].tags` | string[] | All tags (from frontmatter + inline `#tag`) |
| `notes[].frontmatter` | object | Parsed YAML frontmatter key-value pairs |
| `notes[].content` | string | Full note body (markdown, frontmatter stripped) |

---

## Frontmatter keys the skill recognises

The export script preserves all frontmatter. The skill looks for these keys:

| Key | Maps to |
|-----|---------|
| `name` / `full_name` | `profile.name` |
| `email` | `profile.email` |
| `phone` | `profile.phone` |
| `location` / `city` | `profile.location` |
| `linkedin` | `profile.linkedin` |
| `github` | `profile.github` |
| `website` / `url` | `profile.website` |
| `company` | `experience[].company` |
| `title` / `role` / `position` | `experience[].title` |
| `dates` / `period` / `duration` | `experience[].dates` |
| `school` / `university` | `education[].school` |
| `degree` | `education[].degree` |
| `gpa` | `education[].gpa` |

---

## Example note content patterns the skill handles

### Pattern 1: Structured frontmatter
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

### Pattern 2: Heading-based sections
```markdown
# Experience

## Senior Engineer at Startup XYZ (2022–2024)
- Built APIs used by 50k users
- Led CI/CD migration

## Developer at Agency ABC (2020–2022)
- Delivered 12 client projects
```

### Pattern 3: Dataview fields
```markdown
company:: Startup XYZ
role:: Senior Full Stack Engineer
start:: 2022-01
end:: 2024-12

Rebuilt the platform. Led a team.
```

### Pattern 4: Mixed / free-form
```markdown
# About Me
I'm a Full Stack Engineer based in HCMC with 5 years of experience...

**Skills:** Python, React, Docker
**Email:** me@example.com
```

All four patterns are valid. The skill merges data across all collected notes.

---

## Note selection logic

The export script collects a note if ANY of these are true:
- It has a tag in `{career, resume, job, work, experience, skills, education, projects, cv}`
- It lives inside a folder named `Career`, `Job`, `Resume`, `CV`, `Work`, `Experience`, or `Portfolio` (case-insensitive)
- The `--all` flag was passed (collects every `.md` file)
- The `--tag` flag matches one of its tags
