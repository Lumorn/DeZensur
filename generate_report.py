"""Hilfsskript zum Erzeugen eines Batch-Reports.

Dieses Skript ruft intern die CLI `python -m core.report` auf und
speichert den erzeugten Report an einem frei wählbaren Pfad.
"""

import argparse
import subprocess
import sys
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Report erzeugen")
    parser.add_argument("project", help="Pfad zur .dezproj-Datei")
    parser.add_argument("batch_id", help="ID des Batch-Laufs")
    parser.add_argument(
        "--report",
        required=True,
        type=Path,
        help="Zielpfad f\xFCr den JSON-Report",
    )
    parser.add_argument(
        "--html",
        type=Path,
        help="Optionaler Pfad f\xFCr eine HTML-Variante",
    )
    args = parser.parse_args()

    # CLI ausf\xfchren und Pfad zum erzeugten Report erhalten
    result = subprocess.check_output(
        [sys.executable, "-m", "core.report", args.project, args.batch_id],
        text=True,
    ).strip()

    src = Path(result)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    src.replace(args.report)
    if args.html:
        from core.report import render_html

        render_html(args.report, args.html)
        print(args.html)
    else:
        print(args.report)


if __name__ == "__main__":
    main()
