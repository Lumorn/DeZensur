import logging


def get_logger(name: str) -> logging.Logger:
    """Gibt einen Logger mit einfachem Standard-Setup zurück."""
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger(name)
