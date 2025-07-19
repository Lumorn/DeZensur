import json
import statistics
import datetime
from pathlib import Path
from typing import Any

HTML_TEMPLATE = """<html><head><meta charset='utf-8'><title>Batch Report {batch_id}</title></head><body><h1>Batch Report {batch_id}</h1><ul><li>Bilder: {images}</li><li>Durchschnittszeit: {avg_sec} s</li><li>Fehler: {errors}</li></ul><table border='1'><tr><th>Modell</th><th>Anzahl</th></tr>{rows}</table></body></html>"""


def summarize_batch(project_root: Path, batch_id: str) -> Path:
    """Fasst ein Batch-Log in einem Report zusammen."""

    log_path = max((project_root / "logs").glob(f"run_{batch_id}*.jsonl"))
    stats: dict[str, Any] = {"images": 0, "avg_sec": 0, "errors": 0, "models": {}}
    durations: list[float] = []
    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            if rec["level"].lower() == "error":
                stats["errors"] += 1
            if "duration_ms" in rec["extra"]:
                durations.append(rec["extra"]["duration_ms"])
            stats["models"].setdefault(rec["extra"].get("model", "-"), 0)
    stats["images"] = len(durations)
    stats["avg_sec"] = round(statistics.mean(durations) / 1000, 2) if durations else 0
    report = {
        "batch_id": batch_id,
        "created": datetime.datetime.utcnow().isoformat() + "Z",
        **stats,
    }
    rpath = project_root / "logs" / f"{batch_id}_report.json"
    with open(rpath, "w", encoding="utf-8") as fd:
        json.dump(report, fd, indent=2)
    return rpath


def render_html(report_json: Path, html_path: Path) -> Path:
    """Erzeugt eine einfache HTML-Ansicht des Reports."""

    data = json.loads(report_json.read_text())
    rows = "".join(
        f"<tr><td>{model}</td><td>{count}</td></tr>"
        for model, count in data.get("models", {}).items()
    )
    html = HTML_TEMPLATE.format(**data, rows=rows)
    html_path.write_text(html, encoding="utf-8")
    return html_path


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("project")
    parser.add_argument("batch_id")
    args = parser.parse_args()
    path = summarize_batch(Path(args.project).parent, args.batch_id)
    print(path)
