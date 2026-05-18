#!/usr/bin/env python3
"""
Obsidian Vault Exporter — for obsidian-resume skill
----------------------------------------------------
Scans your Obsidian vault and collects career-related notes
into a single JSON file that Claude can read.

Usage
-----
  # Export career-tagged notes (default)
  python export_vault.py --vault ~/Documents/ObsidianVault

  # Export notes with a specific tag
  python export_vault.py --vault ~/Documents/ObsidianVault --tag career

  # Export ALL notes (let Claude decide what's relevant)
  python export_vault.py --vault ~/Documents/ObsidianVault --all

  # Custom output path
  python export_vault.py --vault ~/Documents/ObsidianVault --out ~/Desktop/export.json

Output
------
  obsidian_export.json (same folder as this script, unless --out is set)
"""

import os, re, json, argparse
from pathlib import Path
from datetime import datetime

CAREER_TAGS = {
    "career","resume","job","work","experience",
    "skills","education","projects","cv","portfolio",
}
CAREER_FOLDERS = {
    "career","job","resume","cv","work",
    "experience","about me","portfolio","nghề nghiệp",
}

def parse_frontmatter(content):
    meta = {}
    if not content.startswith("---"):
        return meta, content
    end = content.find("---", 3)
    if end == -1:
        return meta, content
    fm_block = content[3:end].strip()
    body = content[end+3:].strip()
    for line in fm_block.splitlines():
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip().lower()
        value = value.strip().strip('"').strip("'")
        if value.startswith("[") and value.endswith("]"):
            value = [v.strip().strip('"') for v in value[1:-1].split(",") if v.strip()]
        meta[key] = value
    return meta, body

def extract_inline_tags(content):
    return [t.lower() for t in re.findall(r"#([A-Za-z][A-Za-z0-9_/-]*)", content)]

def extract_dataview_fields(content):
    fields = {}
    for m in re.finditer(r"^([A-Za-z_][A-Za-z0-9_ ]*)::\s*(.+)$", content, re.MULTILINE):
        key = m.group(1).strip().lower().replace(" ","_")
        fields[key] = m.group(2).strip()
    return fields

def should_include(path, tags, include_all, filter_tag):
    if include_all: return True
    if filter_tag: return filter_tag.lower() in tags
    if any(t in CAREER_TAGS for t in tags): return True
    parts = {p.lower() for p in path.parts}
    if any(f in parts for f in CAREER_FOLDERS): return True
    return False

def process_note(vault_root, note_path):
    try:
        raw = note_path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return {}
    frontmatter, body = parse_frontmatter(raw)
    inline_tags = extract_inline_tags(body)
    dataview = extract_dataview_fields(body)
    fm_tags = frontmatter.get("tags", [])
    if isinstance(fm_tags, str):
        fm_tags = [t.strip() for t in re.split(r"[,\s]+", fm_tags) if t.strip()]
    all_tags = list({t.lower().strip("#") for t in fm_tags + inline_tags})
    rel_path = note_path.relative_to(vault_root)
    return {
        "filename": note_path.name,
        "path": str(rel_path),
        "tags": all_tags,
        "frontmatter": {**frontmatter, **dataview},
        "content": body,
    }

def export_vault(vault_path, output_path=None, include_all=False, filter_tag=None):
    vault = Path(vault_path).expanduser().resolve()
    if not vault.exists():
        raise FileNotFoundError(f"Vault not found: {vault}")
    notes = []
    skipped = 0
    md_files = list(vault.rglob("*.md"))
    print(f"Found {len(md_files)} markdown files in vault...")
    for md_file in md_files:
        if any(part.startswith(".") for part in md_file.parts):
            continue
        if ".obsidian" in md_file.parts or ".trash" in md_file.parts:
            continue
        note = process_note(vault, md_file)
        if not note:
            skipped += 1
            continue
        if should_include(md_file.relative_to(vault), note["tags"], include_all, filter_tag):
            notes.append(note)
        else:
            skipped += 1
    print(f"Collected {len(notes)} notes ({skipped} skipped).")
    payload = {
        "exported_at": datetime.now().isoformat(timespec="seconds"),
        "vault_name": vault.name,
        "note_count": len(notes),
        "notes": notes,
    }
    out = Path(output_path) if output_path else Path(__file__).parent / "obsidian_export.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n✓ Exported to: {out}")
    print(f"  Paste the contents of this file into Claude to generate your resume.\n")
    return out

def main():
    parser = argparse.ArgumentParser(description="Export Obsidian notes to JSON for Claude resume skill.")
    parser.add_argument("--vault", "-v", required=True, help="Path to your Obsidian vault")
    parser.add_argument("--out", "-o", default=None, help="Output JSON path")
    parser.add_argument("--all", "-a", action="store_true", dest="include_all", help="Export all notes")
    parser.add_argument("--tag", "-t", default=None, help="Only export notes with this tag")
    args = parser.parse_args()
    try:
        export_vault(args.vault, args.out, args.include_all, args.tag)
    except FileNotFoundError as e:
        print(f"Error: {e}"); raise SystemExit(1)

if __name__ == "__main__":
    main()
