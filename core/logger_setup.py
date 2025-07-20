import sys
from pathlib import Path

from loguru import logger

# Standardformat für Konsolen-Ausgaben
DEFAULT_FORMAT = "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {message}"


def init_logging(project_root: Path, debug: bool = False):
    """Initialisiert Loguru mit Text- und JSON-Dateien."""
    log_dir = project_root / "logs"
    log_dir.mkdir(exist_ok=True)

    # Vorhandene Handler entfernen und neue Sinks setzen
    logger.remove()
    logger.add(
        sys.stderr,
        level="DEBUG" if debug else "INFO",
        format=DEFAULT_FORMAT,
        colorize=True,
    )
    logger.add(
        log_dir / "run_{time}.log",
        rotation="10 MB",
        retention="14 days",
        format=DEFAULT_FORMAT,
    )
    logger.add(
        log_dir / "run_{time}.jsonl",
        rotation="100 MB",
        retention="30 days",
        serialize=True,  # Jede Zeile als JSON
    )

    # Zusätzliche Felder vorbereiten
    return logger.patch(lambda r: r["extra"].setdefault("img", "-"))


def get_logger(name: str):
    """Kompatibilitätsfunktion für alte Aufrufer."""
    return logger.bind(mod=name)
