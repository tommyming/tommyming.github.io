#!/usr/bin/env python3
"""Find posts that became due (or expired) since the last Pages deployment.

Usage:
    LAST_DEPLOY="<ISO 8601 timestamp>" python3 check_pending_posts.py

Prints one line per due post to stdout and exits 0. Prints nothing when no
post is due. A post is "due" when it is not a draft and its effective publish
date (``publishDate``, falling back to ``date``) falls in the interval
(LAST_DEPLOY, now]. Posts whose ``expiryDate`` passed in that interval are
also reported, so they get removed from the site by the rebuild.
"""

import os
import pathlib
import re
import sys
import tomllib
from datetime import datetime, timezone

CONTENT_DIR = pathlib.Path("content")
FRONT_MATTER_RE = re.compile(r"\A\+\+\+\r?\n(.*?)\r?\n\+\+\+", re.DOTALL)


def parse_timestamp(raw: str) -> datetime:
    return datetime.fromisoformat(raw.strip().replace("Z", "+00:00"))


def main() -> None:
    since_raw = os.environ.get("LAST_DEPLOY", "").strip()
    if since_raw:
        since = parse_timestamp(since_raw)
    else:
        # No previous deployment found: treat everything published so far as
        # due so the first scheduled run produces a deployment.
        since = datetime(1970, 1, 1, tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)

    for path in sorted(CONTENT_DIR.rglob("*.md")):
        if path.name.startswith("_index"):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"warning: cannot read {path}: {exc}", file=sys.stderr)
            continue
        match = FRONT_MATTER_RE.match(text)
        if not match:
            continue
        try:
            front = {k.lower(): v for k, v in tomllib.loads(match.group(1)).items()}
        except tomllib.TOMLDecodeError as exc:
            print(f"warning: skipping {path}, invalid front matter: {exc}", file=sys.stderr)
            continue
        if front.get("draft", False):
            continue

        publish = front.get("publishdate") or front.get("date")
        expiry = front.get("expirydate")

        if isinstance(publish, datetime) and since < publish <= now:
            print(f"{path} (publish due: {publish.isoformat()})")
        elif isinstance(expiry, datetime) and since < expiry <= now:
            print(f"{path} (expired: {expiry.isoformat()})")


if __name__ == "__main__":
    main()
