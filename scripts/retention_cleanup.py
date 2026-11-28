#!/usr/bin/env python3
"""12-month newsletter retention cleanup for CoupeFab (dry-run by default).

Logs in to the admin API, asks for a count-only plan (or applies deletions),
then logs out. Never prints email addresses or message bodies — counts only.

Usage (from the repo or anywhere, with ADMIN_PASSWORD in the environment):

    python3 scripts/retention_cleanup.py
    python3 scripts/retention_cleanup.py --delete

Optional:

    ADMIN_PASSWORD   required (never pass it on the command line)
    COUPEFAB_BASE    default https://coupefab.ca
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

BASE = os.environ.get("COUPEFAB_BASE", "https://coupefab.ca").rstrip("/")


class Client:
    def __init__(self) -> None:
        self.cookie = ""

    def call(self, path: str, method: str = "GET", body: dict | None = None) -> tuple[int, dict]:
        data = None if body is None else json.dumps(body).encode()
        headers = {"origin": BASE, "accept": "application/json"}
        if data is not None:
            headers["content-type"] = "application/json"
        if self.cookie:
            headers["cookie"] = self.cookie
        req = urllib.request.Request(BASE + path, data=data, method=method, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=120) as res:
                raw = res.read()
                cookie = res.headers.get("set-cookie") or ""
                if "cf_admin=" in cookie:
                    self.cookie = cookie.split(";", 1)[0]
                return res.status, json.loads(raw or b"{}")
        except urllib.error.HTTPError as e:
            raw = e.read()
            try:
                return e.code, json.loads(raw or b"{}")
            except json.JSONDecodeError:
                return e.code, {"ok": False, "error": "http %s" % e.code}


def main() -> int:
    parser = argparse.ArgumentParser(description="CoupeFab 12-month newsletter retention cleanup")
    parser.add_argument("--delete", action="store_true", help="actually delete eligible records (default is dry-run)")
    args = parser.parse_args()
    password = os.environ.get("ADMIN_PASSWORD", "")
    if not password:
        print("ADMIN_PASSWORD is not set. Put it in the environment; do not pass it as a flag.", file=sys.stderr)
        return 2

    c = Client()
    status, body = c.call("/api/admin/login", "POST", {"password": password})
    if status != 200 or not body.get("ok"):
        print("login failed:", status, file=sys.stderr)
        return 1
    try:
        if args.delete:
            status, body = c.call("/api/admin/inbox", "POST", {"action": "retention", "delete": True})
        else:
            status, body = c.call("/api/admin/inbox?action=retention")
    finally:
        c.call("/api/admin/logout", "POST", {})

    if status != 200 or not body.get("ok"):
        print("retention request failed:", status, file=sys.stderr)
        return 1

    mode = "DELETE" if not body.get("dryRun", True) else "DRY-RUN"
    counts = body.get("counts") or {}
    print("CoupeFab retention cleanup (%s)" % mode)
    if body.get("cutoff"):
        print("cutoff (UTC):", body["cutoff"])
    for key in sorted(counts):
        print("%s: %s" % (key, counts[key]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
