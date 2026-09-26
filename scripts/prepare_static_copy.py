#!/usr/bin/env python3
"""Rewrite same-host absolute URLs as root-relative URLs for static hosting."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit


ORIGIN = re.compile(r"(?i)(?:https?:)?//star\.mit\.edu(?=/|[?#\"'<>\s]|$)")
TEXT_SUFFIXES = {".html", ".htm", ".css", ".js"}
URL_ATTRIBUTE = re.compile(
    r"(?P<prefix>\b(?:href|src|action|poster|data)\s*=\s*)(?P<quote>[\"'])(?P<url>.*?)(?P=quote)",
    re.IGNORECASE | re.DOTALL,
)
STATIC_FALLBACKS = {
    "/cluster/docs": "/cluster/docs/latest/",
    "/cluster/download.html": "/cluster/downloads.html",
}


def make_static_url(value: str, page: Path, root: Path) -> str:
    if "%3f" in value.lower():
        value = re.sub(r"%3f", "?", value, flags=re.IGNORECASE)
        value = re.sub(r"\.tmp\.html(?=#|$)", "", value, flags=re.IGNORECASE)

    parts = urlsplit(value)
    if parts.netloc and parts.hostname and parts.hostname.lower() == "star.mit.edu":
        parts = parts._replace(scheme="", netloc="", path=parts.path or "/")

    path = parts.path
    if path in STATIC_FALLBACKS:
        parts = parts._replace(path=STATIC_FALLBACKS[path])
        path = parts.path

    if path and not path.endswith("/"):
        local = (root / path.lstrip("/")) if path.startswith("/") else (page.parent / path)
        html_target = local.with_name(local.name + ".html")
        if local.is_dir() and (local / "index.html").is_file():
            parts = parts._replace(path=path + "/")
        elif not Path(path).suffix and html_target.is_file():
            parts = parts._replace(path=path + ".html")

    return urlunsplit(parts)


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    files_changed = 0
    replacements = 0
    path_adjustments = 0

    for path in root.rglob("*"):
        if not path.is_file() or ".git" in path.parts or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            original = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        def root_relative(match: re.Match[str]) -> str:
            nonlocal replacements
            replacements += 1
            following = original[match.end():match.end() + 1]
            return "" if following == "/" else "/"

        updated = ORIGIN.sub(root_relative, original)

        def normalize_attribute(match: re.Match[str]) -> str:
            nonlocal path_adjustments
            value = match.group("url")
            normalized = make_static_url(value, path, root)
            if normalized != value:
                path_adjustments += 1
            return f"{match.group('prefix')}{match.group('quote')}{normalized}{match.group('quote')}"

        updated = URL_ATTRIBUTE.sub(normalize_attribute, updated)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            files_changed += 1

    print(
        f"Rewrote {replacements} same-host URL strings and normalized "
        f"{path_adjustments} local link paths in {files_changed} files."
    )
    print(f"Archive root: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
