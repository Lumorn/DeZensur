"""Minimaler Ersatz für das Requests-Modul, nutzt urllib."""

from __future__ import annotations

import json as jsonlib
import urllib.request
from types import SimpleNamespace


class Response:
    def __init__(self, resp: urllib.request.addinfourl):
        self._resp = resp
        self.status_code = getattr(resp, "status", 200)
        self.headers = dict(resp.headers)
        self.ok = self.status_code < 400

    def json(self) -> dict:
        data = self._resp.read().decode()
        return jsonlib.loads(data)

    def iter_content(self, chunk_size: int = 8192):
        while True:
            chunk = self._resp.read(chunk_size)
            if not chunk:
                break
            yield chunk

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise Exception(f"Status {self.status_code}")

    def close(self) -> None:
        self._resp.close()

    def __enter__(self) -> "Response":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()


def _request(method: str, url: str, data=None, headers=None, timeout: int | None = None) -> Response:
    req = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    resp = urllib.request.urlopen(req, timeout=timeout)
    return Response(resp)


def head(url: str, allow_redirects: bool = True, timeout: int | None = None) -> Response:
    return _request("HEAD", url, timeout=timeout)


def get(url: str, headers=None, stream: bool = False) -> Response:
    return _request("GET", url, headers=headers)


def post(url: str, json: dict | None = None) -> Response:
    data = None
    hdrs = {}
    if json is not None:
        data = jsonlib.dumps(json).encode()
        hdrs["Content-Type"] = "application/json"
    return _request("POST", url, data=data, headers=hdrs)
