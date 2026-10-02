#!/usr/bin/env python3
"""Local static server with HTTP Range support (bytes=a-b).

CheerpJ loads JARs with Range requests, which `python3 -m http.server`
ignores, so use this to preview the browser-based Java apps locally.
Usage: serve_with_range.py PORT DIRECTORY
"""
import functools, os, re, sys
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

class RangeHandler(SimpleHTTPRequestHandler):
    def send_head(self):
        self._range = None
        m = re.fullmatch(r"bytes=(\d*)-(\d*)", self.headers.get("Range", "").strip())
        path = self.translate_path(self.path)
        if not m or os.path.isdir(path) or not os.path.isfile(path):
            return super().send_head()
        size = os.path.getsize(path)
        start, end = m.groups()
        if start == "":
            start, end = max(0, size - int(end or 0)), size - 1
        else:
            start, end = int(start), min(int(end) if end else size - 1, size - 1)
        if start >= size or start > end:
            self.send_response(HTTPStatus.REQUESTED_RANGE_NOT_SATISFIABLE)
            self.send_header("Content-Range", f"bytes */{size}")
            self.send_header("Content-Length", "0")
            self.end_headers()
            return None
        f = open(path, "rb")
        f.seek(start)
        self._range = end - start + 1
        self.send_response(HTTPStatus.PARTIAL_CONTENT)
        self.send_header("Content-Type", self.guess_type(path))
        self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.send_header("Content-Length", str(self._range))
        self.send_header("Accept-Ranges", "bytes")
        self.end_headers()
        return f

    def send_error(self, code, message=None, explain=None):
        # Like Cloudflare Pages: answer missing paths with the site's 404.html.
        page = os.path.join(self.directory, "404.html")
        if code != HTTPStatus.NOT_FOUND or not os.path.isfile(page):
            return super().send_error(code, message, explain)
        with open(page, "rb") as f:
            body = f.read()
        self._range = None
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def copyfile(self, source, outputfile):
        if getattr(self, "_range", None) is None:
            return super().copyfile(source, outputfile)
        remaining = self._range
        while remaining > 0:
            buf = source.read(min(65536, remaining))
            if not buf:
                break
            outputfile.write(buf)
            remaining -= len(buf)

    def end_headers(self):
        if getattr(self, "_range", None) is None:
            self.send_header("Accept-Ranges", "bytes")
        super().end_headers()

if __name__ == "__main__":
    port, directory = int(sys.argv[1]), sys.argv[2]
    handler = functools.partial(RangeHandler, directory=directory)
    ThreadingHTTPServer(("", port), handler).serve_forever()
