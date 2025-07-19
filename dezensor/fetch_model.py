"""Lädt ein Modell manuell aus dem Registry."""

from __future__ import annotations

import argparse

from core import dep_manager


def main() -> None:
    parser = argparse.ArgumentParser(description="Modell herunterladen")
    parser.add_argument("key", help="Schlüssel im MODEL_REGISTRY")
    parser.add_argument(
        "--cpu",
        action="store_true",
        help="GPU-Modelle trotz fehlender GPU laden",
    )
    args = parser.parse_args()

    path = dep_manager.ensure_model(args.key, prefer_gpu=not args.cpu)
    print(path)


if __name__ == "__main__":
    main()
