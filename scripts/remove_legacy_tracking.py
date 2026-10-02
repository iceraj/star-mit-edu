"""Remove obsolete Google Analytics and Sentry loaders from archived HTML.

The STAR capture contains two GA generations: the original synchronous
``ga.js`` / ``_gat`` pair and the later asynchronous ``_gaq`` block. The
shared ``on_every_page.js`` file loads an old Raven/Sentry client. This
script removes only those known script blocks, preserving each page's
original bytes otherwise (including non-UTF-8 text and line endings).
"""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = re.compile(
    rb"(?m)^[ \t]*<script\b[^>]*>.*?</script\s*>[ \t]*(?:\r?\n)?"
    rb"|<script\b[^>]*>.*?</script\s*>",
    re.IGNORECASE | re.DOTALL,
)
COUNTS = {"ga_loader": 0, "ga_pageview": 0, "sentry_loader": 0}


def without_tracking(match: re.Match[bytes]) -> bytes:
    block = match.group()
    if b"google-analytics.com/ga.js" in block:
        if b"gaJsHost" not in block and b"_gaq" not in block:
            raise ValueError("Unrecognized Google Analytics block")
        COUNTS["ga_loader"] += 1
        return b""
    if b"_gat._getTracker" in block:
        if b"pageTracker._trackPageview()" not in block:
            raise ValueError("Unrecognized Google Analytics pageview block")
        COUNTS["ga_pageview"] += 1
        return b""
    if b"on_every_page.js" in block:
        if not re.search(rb"\bsrc\s*=", block, re.IGNORECASE):
            raise ValueError("Unrecognized shared Sentry loader")
        COUNTS["sentry_loader"] += 1
        return b""
    return block


changed = 0
for path in ROOT.rglob("*.html"):
    original = path.read_bytes()
    if not any(
        marker in original
        for marker in (b"google-analytics.com/ga.js", b"_gat._getTracker", b"on_every_page.js")
    ):
        continue
    updated = SCRIPT.sub(without_tracking, original)
    # Mailing-list pages put the GA pair between an existing blank line and
    # their jQuery includes. Keep that original spacing after removing GA.
    if path.parent.name == "mlarchives":
        updated = updated.replace(
            b'\r\n\r\n\r\n<script src="jquery.min.js"',
            b'\r\n\r\n<script src="jquery.min.js"',
        )
    if updated != original:
        path.write_bytes(updated)
        changed += 1

print(f"Updated {changed} HTML pages: " + ", ".join(f"{key}={value}" for key, value in COUNTS.items()))
