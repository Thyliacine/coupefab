#!/usr/bin/env python3
"""Print the arguments for the Vercel connector's create_deployment call.

The site is deployed from this directory (no Git integration). Each file is
inlined with the "$file:/abs/path" convention that the agent tool runner
expands, so the JSON stays small.

    python3 scripts/deploy_manifest.py > /tmp/coupefab-deploy.json
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INCLUDE_TOP = ["index.html", "404.html", "favicon.svg", "robots.txt", "sitemap.xml", "vercel.json"]
INCLUDE_DIRS = ["a-propos", "api", "confidentialite", "css", "divulgation", "en", "guides", "infolettre", "js",
                "occasions", "prix"]


def files():
    out = []
    for name in INCLUDE_TOP:
        if (ROOT / name).exists():
            out.append(ROOT / name)
    for d in INCLUDE_DIRS:
        for p in sorted((ROOT / d).rglob("*")):
            if p.is_file() and not p.name.startswith("."):
                out.append(p)
    return out


def main():
    body = {
        "name": "coupefab",
        "project": "coupefab",
        "target": "production",
        "files": [{"file": str(p.relative_to(ROOT)), "data": f"$file:{p}", "encoding": "utf-8"} for p in files()],
        "projectSettings": {"framework": None, "buildCommand": None, "outputDirectory": None, "installCommand": None},
    }
    print(json.dumps({"slug": "micro-bot", "skipAutoDetectionConfirmation": "1", "requestBody": body}, indent=1))


if __name__ == "__main__":
    main()
