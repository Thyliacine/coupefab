#!/usr/bin/env python3
"""Pack the built static site as site.tgz for the Vercel connector.

Recent CoupeFab production deploys unpack a single tarball:

    mkdir -p public && tar xzf site.tgz -C public

The payload is three files under src/ (rootDirectory=src):

    src/site.tgz
    src/vercel.json          (scripts/vercel-deploy.json — not the repo-root vercel.json)
    src/api/subscribe.js

This avoids the 199-file SHA manifest, which Vercel now reports as
missing_files because current production deploys only cache the tarball.

Writes /tmp/coupefab-deploy/:
  site.tgz
  <sha>.b64 for each of the three files
  uploads.json
  create_deployment.json
  requestBody.json

Procedure (agent):
  1. upload_file for any new SHA (xVercelDigest, contentLength, requestBody=$file:<b64_path>,
     teamId=team_51rPr828F5cibUCQd4qzdhyb);
  2. create_deployment with teamId, skipAutoDetectionConfirmation=1, forceNew=1,
     and requestBody=$file:/tmp/coupefab-deploy/requestBody.json.
"""
from __future__ import annotations

import base64
import hashlib
import json
import tarfile
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = Path("/tmp/coupefab-deploy")
TEAM = "team_51rPr828F5cibUCQd4qzdhyb"
DEPLOY_VERCEL = Path(__file__).resolve().parent / "vercel-deploy.json"

INCLUDE_TOP = [
    "index.html", "404.html", "favicon.svg", "apple-touch-icon.png",
    "site.webmanifest", "robots.txt", "sitemap.xml",
]
INCLUDE_DIRS = [
    "a-propos", "api", "confidentialite", "css", "divulgation", "en",
    "fonts", "guides", "infolettre", "js", "og", "occasions", "prix",
]


def site_files():
    out = [ROOT / n for n in INCLUDE_TOP if (ROOT / n).exists()]
    for d in INCLUDE_DIRS:
        folder = ROOT / d
        if not folder.exists():
            continue
        out += [p for p in sorted(folder.rglob("*")) if p.is_file() and not p.name.startswith(".")]
    return out


def _ref(rel: str, data: bytes, uploads: list) -> dict:
    sha = hashlib.sha1(data).hexdigest()
    b64 = OUT / f"{sha}.b64"
    b64.write_text(base64.b64encode(data).decode())
    rec = {"file": rel, "sha": sha, "size": len(data), "b64_path": str(b64)}
    uploads.append(rec)
    return {"file": rel, "sha": sha, "size": len(data)}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    # Pack without a leading ./ so `tar xzf site.tgz -C public` matches the live layout.
    tmp = Path(tempfile.mkdtemp(prefix="coupefab-tgz-"))
    tgz_path = tmp / "site.tgz"
    with tarfile.open(tgz_path, "w:gz") as tar:
        for p in site_files():
            tar.add(p, arcname=str(p.relative_to(ROOT)), recursive=False)
    site_bytes = tgz_path.read_bytes()
    (OUT / "site.tgz").write_bytes(site_bytes)

    vercel_bytes = DEPLOY_VERCEL.read_bytes()
    api_bytes = (ROOT / "api" / "subscribe.js").read_bytes()

    uploads: list[dict] = []
    refs = [
        _ref("src/site.tgz", site_bytes, uploads),
        _ref("src/vercel.json", vercel_bytes, uploads),
        _ref("src/api/subscribe.js", api_bytes, uploads),
    ]
    request_body = {
        "name": "coupefab",
        "project": "coupefab",
        "target": "production",
        "files": refs,
        "projectSettings": {
            "framework": None,
            "buildCommand": "mkdir -p public && tar xzf site.tgz -C public",
            "outputDirectory": "public",
            "installCommand": "",
            "rootDirectory": "src",
        },
    }
    args = {
        "teamId": TEAM,
        "skipAutoDetectionConfirmation": "1",
        "forceNew": "1",
        "requestBody": request_body,
    }
    (OUT / "create_deployment.json").write_text(json.dumps(args, indent=1))
    (OUT / "requestBody.json").write_text(json.dumps(request_body, indent=1))
    (OUT / "uploads.json").write_text(json.dumps(uploads, indent=1))
    print(f"site.tgz {refs[0]['size']} bytes sha={refs[0]['sha']} -> {OUT}/create_deployment.json (3 files)")


if __name__ == "__main__":
    main()
