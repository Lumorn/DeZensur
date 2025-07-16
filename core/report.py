import json
import statistics
import datetime
from pathlib import Path


def summarize_batch(project_root: Path, batch_id: str):
    """Fasst ein Batch-Log in einem Report zusammen."""
    log_path = max((project_root / "logs").glob(f"run_{batch_id}*.jsonl"))
    stats = {"images": 0, "avg_sec": 0, "errors": 0, "models": {}}
    durations = []
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


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("project")
    parser.add_argument("batch_id")
    args = parser.parse_args()
    path = summarize_batch(Path(args.project).parent, args.batch_id)
    print(path)
