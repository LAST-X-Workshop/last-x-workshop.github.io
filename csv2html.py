#!/usr/bin/env python3
"""
csv_to_html_list.py

Convert a CSV (with columns: given_name, family_name, affiliation) into HTML:

<ul style="list-style-type:none; text-align:center;">
  <li><strong>First Last</strong> — Affiliation</li>
  ...
</ul>

Usage:
  python csv_to_html_list.py /path/to/lastx2026-users.csv > output.html
"""

import csv
import html
import sys


TEMPLATE_OPEN = '<ul style="list-style-type:none; text-align:center;">'
TEMPLATE_CLOSE = "</ul>"


def csv_to_html_ul(csv_path: str) -> str:
    lines = [TEMPLATE_OPEN]
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        required = {"given_name", "family_name", "affiliation"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"CSV missing required columns: {sorted(missing)}")

        for row in reader:
            given = (row.get("given_name") or "").strip()
            family = (row.get("family_name") or "").strip()
            aff = (row.get("affiliation") or "").strip()

            # Skip rows with no name at all
            name = " ".join([p for p in [given, family] if p]).strip()
            if not name:
                continue

            # Escape to keep HTML safe (e.g., Texas A&M -> Texas A&amp;M)
            name_esc = html.escape(name, quote=True)
            aff_esc = html.escape(aff, quote=True)

            lines.append(f'\t<li><strong>{name_esc}</strong> — {aff_esc}</li>')

    lines.append(TEMPLATE_CLOSE)
    return "\n".join(lines)


def main():
    if len(sys.argv) != 2:
        print("Usage: python csv_to_html_list.py INPUT.csv", file=sys.stderr)
        sys.exit(2)

    csv_path = sys.argv[1]
    try:
        print(csv_to_html_ul(csv_path))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()