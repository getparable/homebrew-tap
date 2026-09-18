#!/usr/bin/env python3
"""Check that each formula's bottle exists and matches the version it ships.

Homebrew does not complain when a bottle is missing, misnamed or stale. It falls back
to building from source, so `brew install` still succeeds — it just takes minutes and
needs a full Xcode, which is the prerequisite the bottle exists to remove. Nothing
reports a problem; the only symptom is `==> Installing` where `==> Pouring` belonged.

So the two ways to get this wrong are both silent, and this catches them before anyone
installs:

  * `url` and the bottle's `root_url` naming different versions, which happens whenever
    the formula is bumped and the bottle block is not; and
  * a correctly named bottle that was never uploaded to the release, or was uploaded
    under the local double-dash filename rather than the single-dash one Homebrew asks
    for.

Run it locally the same way CI does: python3 scripts/check-formula.py
"""

from __future__ import annotations

import pathlib
import re
import sys
import time
import urllib.error
import urllib.request

FORMULA_DIR = pathlib.Path(__file__).resolve().parent.parent / "Formula"

SOURCE_URL = re.compile(r'url\s+"[^"]*/archive/refs/tags/v(?P<version>[0-9][^"/]*)\.tar\.gz"')
ROOT_URL = re.compile(r'root_url\s+"(?P<root>[^"]*/releases/download/v(?P<version>[0-9][^"/]*))"')
BOTTLE_TAG = re.compile(r"(?P<tag>[a-z0-9_]+):\s*\"(?P<sha>[0-9a-f]{64})\"")


def head(url: str, attempts: int = 3) -> int:
    """Status code for url, following redirects. Release assets redirect to a CDN."""
    request = urllib.request.Request(url, method="HEAD")
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return response.status
        except urllib.error.HTTPError as error:
            return error.code
        except urllib.error.URLError:
            # A flaky network should not read as a missing bottle.
            if attempt == attempts - 1:
                raise
            time.sleep(2 * (attempt + 1))
    return 0


def check(path: pathlib.Path) -> list[str]:
    text = path.read_text()
    name = path.stem
    problems: list[str] = []

    source = SOURCE_URL.search(text)
    if not source:
        return [f"{path}: no source `url` matching .../archive/refs/tags/vX.Y.Z.tar.gz"]
    version = source.group("version")

    root = ROOT_URL.search(text)
    if not root:
        # A formula may legitimately ship without a bottle; it just builds from source.
        print(f"{path}: no bottle block — installs will build from source")
        return problems

    if root.group("version") != version:
        problems.append(
            f"{path}: url is v{version} but the bottle's root_url is "
            f"v{root.group('version')}.\n"
            f"  Homebrew will not find a bottle for v{version} and will silently build "
            f"from source instead.\n"
            f"  Build and upload the bottle for v{version}, then update root_url and its "
            f"sha256 (README → Releasing)."
        )
        return problems

    tags = BOTTLE_TAG.findall(text[root.end():])
    if not tags:
        problems.append(f"{path}: bottle block names no platform tag")
        return problems

    for tag, _sha in tags:
        # Homebrew requests one dash here; `brew bottle` writes two locally.
        filename = f"{name}-{version}.{tag}.bottle.tar.gz"
        url = f"{root.group('root')}/{filename}"
        status = head(url)
        if status == 200:
            print(f"{path}: {tag} bottle present — {filename}")
            continue
        problems.append(
            f"{path}: the {tag} bottle for v{version} is not downloadable "
            f"(HTTP {status}).\n"
            f"  Expected: {url}\n"
            f"  Every install will quietly build from source until it is there. Check the\n"
            f"  asset is attached to the v{version} release and named with ONE dash "
            f"({filename}),\n"
            f"  not the two that `brew bottle` writes locally."
        )
    return problems


def main() -> int:
    formulae = sorted(FORMULA_DIR.glob("*.rb"))
    if not formulae:
        print(f"no formulae under {FORMULA_DIR}", file=sys.stderr)
        return 1

    problems: list[str] = []
    for path in formulae:
        problems.extend(check(path.relative_to(pathlib.Path.cwd()) if path.is_relative_to(pathlib.Path.cwd()) else path))

    if problems:
        print("", file=sys.stderr)
        for problem in problems:
            print(f"error: {problem}", file=sys.stderr)
        return 1

    print(f"\n{len(formulae)} formula(e) checked, bottles present and matching.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
