"""Extrahiert den Changelog-Eintrag zu einem gegebenen Tag."""

import re
import sys
from pathlib import Path

# Tag-Name vom Git-Event (z.B. v1.2.3)
tag = sys.argv[1]
tag = tag.lstrip("v")
text = Path("CHANGELOG.md").read_text(encoding="utf-8").splitlines()
# Regex zum Finden der Versionszeilen
pat = re.compile(r"^## \[(?P<ver>.+?)\]")
start = None
for i, line in enumerate(text):
    # Start-Zeile der gewünschten Version finden
    m = pat.match(line)
    if m and m.group("ver") == tag:
        start = i + 1
        break
if start is None:
    sys.exit(f"Version {tag} nicht gefunden")
body_lines = []
for line in text[start:]:
    if pat.match(line):
        break
    body_lines.append(line.rstrip())  # Zeile übernehmen
print("\n".join(body_lines).strip())
