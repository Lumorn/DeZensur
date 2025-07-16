from pathlib import Path
import json
import datetime
import sys


class _Logger:
    def __init__(self, sinks=None, extra=None):
        self.sinks = sinks or []
        self.extra = extra or {}

    def remove(self):
        self.sinks.clear()

    def add(self, sink, serialize=False, **kwargs):
        if hasattr(sink, "write"):
            # Konsole ignorieren
            return
        name = str(sink)
        if "{time}" in name:
            name = name.replace("{time}", datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S"))
        self.sinks.append((Path(name), serialize))

    def bind(self, **extra):
        new_extra = self.extra.copy()
        new_extra.update(extra)
        return _Logger(self.sinks, new_extra)

    def patch(self, func):
        # Patch wird ignoriert, aber für Kompatibilität zurückgegeben
        return self

    def _log(self, level, message, *args, **extra):
        if args:
            try:
                message = message.format(*args)
            except Exception:
                message = message % args
        data = {"level": level, "message": message, "extra": {**self.extra, **extra}}
        for path, serialize in self.sinks:
            path.parent.mkdir(parents=True, exist_ok=True)
            if serialize:
                rec = {"time": datetime.datetime.utcnow().isoformat() + "Z", **data}
                with open(path, "a", encoding="utf-8") as f:
                    f.write(json.dumps(rec) + "\n")
            else:
                with open(path, "a", encoding="utf-8") as f:
                    f.write(message + "\n")

    def info(self, message, *args, **extra):
        self._log("INFO", message, *args, **extra)

    def error(self, message, *args, **extra):
        self._log("ERROR", message, *args, **extra)

    def exception(self, message, *args, **extra):
        self._log("ERROR", message, *args, **extra)


logger = _Logger()
