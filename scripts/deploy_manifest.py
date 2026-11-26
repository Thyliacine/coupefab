#!/usr/bin/env python3
"""Prepare a Vercel deployment of this static site through the Vercel connector.

The site is deployed from this directory (the Vercel Git integration is not installed).
Writes:
  /tmp/coupefab-deploy/create_deployment.json  arguments for the connector's create_deployment
                                               (files referenced by SHA1 + size, no inline data)
  /tmp/coupefab-deploy/uploads.json            [{file, sha, size, b64_path}] for upload_file
  /tmp/coupefab-deploy/<sha>.b64               base64 body of each file

Procedure (agent):
  1. call create_deployment with create_deployment.json;
  2. if Vercel answers "missing_files" with a list of SHAs, call upload_file for each of them
     (xVercelDigest=sha, contentLength=size, requestBody="$file:<b64_path>", teamId=team_51rPr828F5cibUCQd4qzdhyb),
     then repeat step 1.
"""
import base64
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = Path("/tmp/coupefab-deploy")
INCLUDE_TOP = ["index.html", "404.html", "favicon.svg", "robots.txt", "sitemap.xml", "vercel.json"]
INCLUDE_DIRS = ["a-propos", "api", "confidentialite", "css", "divulgation", "en", "guides", "infolettre", "js",
                "occasions", "prix"]


def files():
    out = [ROOT / n for n in INCLUDE_TOP if (ROOT / n).exists()]
    for d in INCLUDE_DIRS:
        out += [p for p in sorted((ROOT / d).rglob("*")) if p.is_file() and not p.name.startswith(".")]
    return out


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    refs, uploads = [], []
    for p in files():
        b = p.read_bytes()
        sha = hashlib.sha1(b).hexdigest()
        b64 = OUT / f"{sha}.b64"
        b64.write_text(base64.b64encode(b).decode())
        rel = str(p.relative_to(ROOT))
        refs.append({"file": rel, "sha": sha, "size": len(b)})
        uploads.append({"file": rel, "sha": sha, "size": len(b), "b64_path": str(b64)})
    args = {"teamId": "team_51rPr828F5cibUCQd4qzdhyb", "skipAutoDetectionConfirmation": "1",
            "requestBody": {"name": "coupefab", "project": "coupefab", "target": "production", "files": refs,
                            "projectSettings": {"framework": None}}}
    (OUT / "create_deployment.json").write_text(json.dumps(args, indent=1))
    (OUT / "uploads.json").write_text(json.dumps(uploads, indent=1))
    print(f"{len(refs)} files -> {OUT}/create_deployment.json (uploads listed in uploads.json)")


if __name__ == "__main__":
    main()
