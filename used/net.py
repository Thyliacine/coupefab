"""Polite HTTP: identified UA, robots.txt + Crawl-delay, no login, no bot-wall bypass."""
from __future__ import annotations

import time
import urllib.robotparser
from urllib.parse import urlparse

import requests

USER_AGENT = "Mozilla/5.0 (compatible; CoupeFabOccasionsBot/1.0; +https://coupefab.ca/occasions/)"
DEFAULT_DELAY = 1.5

S = requests.Session()
S.headers.update({
    "User-Agent": USER_AGENT,
    "Accept-Language": "fr-CA,fr;q=0.9,en;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/json,application/xml;q=0.9,*/*;q=0.8",
})

_robots: dict = {}
_last_hit: dict = {}


class Blocked(Exception):
    """robots.txt, HTTP challenge, or transport failure that we will not work around."""


def origin(url: str) -> str:
    p = urlparse(url)
    return f"{p.scheme}://{p.netloc}"


def robots_for(base: str) -> urllib.robotparser.RobotFileParser:
    if base not in _robots:
        rp = urllib.robotparser.RobotFileParser()
        try:
            r = S.get(base + "/robots.txt", timeout=20)
            if r.status_code == 200 and "text" in (r.headers.get("content-type") or "text"):
                rp.parse(r.text.splitlines())
            else:
                # Non-200 robots.txt is not a licence to crawl aggressively, but an
                # empty rule-set is the RFC fallback; the later GET still records 403/202.
                rp.parse([])
        except requests.RequestException:
            rp.parse([])
        _robots[base] = rp
    return _robots[base]


def robots_ok(url: str) -> bool:
    try:
        return bool(robots_for(origin(url)).can_fetch(USER_AGENT, url))
    except Exception:
        return False


def is_challenge(resp: requests.Response) -> str | None:
    if resp.status_code in (401, 403, 429, 503):
        return f"HTTP {resp.status_code}"
    if resp.status_code == 202 and len(resp.content) < 8000:
        return "HTTP 202 challenge"
    text = ""
    ctype = (resp.headers.get("content-type") or "").lower()
    if "html" in ctype or "text" in ctype:
        text = resp.text[:4000].lower()
    needles = (
        "cf-browser-verification", "just a moment", "attention required",
        "access denied", "pardon our interruption", "captcha",
        "enable javascript and cookies", "verify you are a human",
        "checking your browser",
    )
    if any(n in text for n in needles):
        return "challenge page"
    return None


def get(url: str, *, timeout: int = 40, allow_redirects: bool = True, headers=None) -> requests.Response:
    base = origin(url)
    rp = robots_for(base)
    if not rp.can_fetch(USER_AGENT, url):
        raise Blocked(f"robots.txt disallows {url}")
    delay = max(DEFAULT_DELAY, float(rp.crawl_delay(USER_AGENT) or 0))
    wait = _last_hit.get(base, 0) + delay - time.time()
    if wait > 0:
        time.sleep(wait)
    try:
        r = S.get(url, timeout=timeout, allow_redirects=allow_redirects, headers=headers)
    except requests.RequestException as e:
        _last_hit[base] = time.time()
        raise Blocked(f"{type(e).__name__}: {e}") from e
    _last_hit[base] = time.time()
    why = is_challenge(r)
    if why:
        raise Blocked(f"{why} for {url}")
    return r
