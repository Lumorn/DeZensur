import argparse
import json
from pathlib import Path

from core.censor_detector import detect_censor
from core.inpainter import inpaint, SUPPORTED_MODELS


def _cmd_detect(args: argparse.Namespace) -> None:
    """Durchsucht einen Ordner nach Bildern und erzeugt einen JSON-Report."""
    folder = Path(args.folder)
    exts = {".png", ".jpg", ".jpeg", ".webp"}
    data = {}
    for img in sorted(folder.iterdir()):
        if img.suffix.lower() not in exts:
            continue
        roi = None
        if args.roi:
            parts = [float(v) for v in args.roi.split(",")]
            if len(parts) == 4:
                roi = tuple(parts)  # type: ignore[assignment]
        boxes = detect_censor(img, threshold=args.threshold, roi=roi)
        data[img.name] = boxes
    out = json.dumps(data, ensure_ascii=False, indent=2)
    if args.out:
        Path(args.out).write_text(out, encoding="utf-8")
    else:
        print(out)


def _cmd_inpaint(args: argparse.Namespace) -> None:
    """Inpaintet ein einzelnes Bild mithilfe einer Maske."""
    out = inpaint(
        Path(args.image),
        Path(args.mask),
        None,
        args.model,
        args.prompt,
    )
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        from PIL import Image

        Image.open(out).save(args.out)
        print(args.out)
    else:
        print(out)


def main() -> int:
    parser = argparse.ArgumentParser(prog="dez")
    sub = parser.add_subparsers(dest="cmd")

    p_detect = sub.add_parser("detect", help="Ordnerweise Zensur erkennen")
    p_detect.add_argument("folder")
    p_detect.add_argument("--out", help="Pfad für den JSON-Report")
    p_detect.add_argument("--threshold", type=float, default=0.3)
    p_detect.add_argument("--roi", help="x1,y1,x2,y2 im Bereich 0-1")
    p_detect.set_defaults(func=_cmd_detect)

    p_inpaint = sub.add_parser("inpaint", help="Einzelnes Bild inpainten")
    p_inpaint.add_argument("image")
    p_inpaint.add_argument("--mask", required=True)
    p_inpaint.add_argument(
        "--model",
        default="lama",
        choices=list(SUPPORTED_MODELS.keys()),
    )
    p_inpaint.add_argument("--prompt", default="")
    p_inpaint.add_argument("--out")
    p_inpaint.set_defaults(func=_cmd_inpaint)

    args = parser.parse_args()
    if not args.cmd:
        parser.print_help()
        return 1
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
