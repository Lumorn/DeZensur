import argparse
import json
from pathlib import Path

from core.censor_detector import detect_censor


def _cmd_detect(args: argparse.Namespace) -> None:
    """Durchsucht einen Ordner nach Bildern und erzeugt einen JSON-Report."""
    folder = Path(args.folder)
    exts = {".png", ".jpg", ".jpeg", ".webp"}
    data = {}
    for img in sorted(folder.iterdir()):
        if img.suffix.lower() not in exts:
            continue
        boxes = detect_censor(img, threshold=args.threshold)
        data[img.name] = boxes
    out = json.dumps(data, ensure_ascii=False, indent=2)
    if args.out:
        Path(args.out).write_text(out, encoding="utf-8")
    else:
        print(out)


def main() -> int:
    parser = argparse.ArgumentParser(prog="dez")
    sub = parser.add_subparsers(dest="cmd")

    p_detect = sub.add_parser("detect", help="Ordnerweise Zensur erkennen")
    p_detect.add_argument("folder")
    p_detect.add_argument("--out", help="Pfad für den JSON-Report")
    p_detect.add_argument("--threshold", type=float, default=0.3)
    p_detect.set_defaults(func=_cmd_detect)

    args = parser.parse_args()
    if not args.cmd:
        parser.print_help()
        return 1
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
