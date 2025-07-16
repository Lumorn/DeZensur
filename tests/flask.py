"""Minimaler Ersatz für Flask, nutzt http.server."""
from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from types import SimpleNamespace


class _Request:
    def __init__(self) -> None:
        self._json = {}

    def get_json(self) -> dict:
        return self._json


request = _Request()


def jsonify(obj: dict) -> dict:
    return obj


class Flask:
    def __init__(self, name: str) -> None:
        self._routes: dict[str, callable] = {}

    def post(self, path: str):
        def decorator(func):
            self._routes[path] = func
            return func

        return decorator

    def run(self, port: int = 5000) -> None:
        app = self

        class Handler(BaseHTTPRequestHandler):
            def do_POST(self) -> None:
                length = int(self.headers.get("Content-Length", 0))
                data = self.rfile.read(length) if length else b""
                request._json = json.loads(data.decode() or "{}")
                if self.path in app._routes:
                    resp = app._routes[self.path]()
                    body = json.dumps(resp).encode()
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.send_header("Content-Length", str(len(body)))
                    self.end_headers()
                    self.wfile.write(body)
                else:
                    self.send_error(404)

        server = HTTPServer(("127.0.0.1", port), Handler)
        server.serve_forever()
