#!/usr/bin/env python3
"""Read-only inventory for pages-ai root notes and PARA index coverage."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


INDEXES = {
    "Projects": Path("pages-ai/01-projects/01-Projects(项目).md"),
    "Areas": Path("pages-ai/02-areas/02-Areas(领域).md"),
    "Resources": Path("pages-ai/03-resources/03-Resources(资源).md"),
}
WIKILINK = re.compile(r"(?<!!)\[\[([^\]]+)\]\]")


def link_title(raw: str) -> str:
    target = raw.split("|", 1)[0].split("#", 1)[0].strip().replace("\\", "/")
    name = target.rsplit("/", 1)[-1]
    return name[:-3] if name.lower().endswith(".md") else name


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vault", type=Path, default=Path.cwd())
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    vault = args.vault.expanduser().resolve()
    pages = vault / "pages-ai"
    missing = [str(path) for path in INDEXES.values() if not (vault / path).is_file()]
    links: dict[str, set[str]] = {}
    for category, relative in INDEXES.items():
        path = vault / relative
        if not path.is_file():
            continue
        for raw in WIKILINK.findall(path.read_text(encoding="utf-8")):
            links.setdefault(link_title(raw), set()).add(category)

    candidates = []
    if pages.is_dir():
        for path in sorted(pages.glob("*.md"), key=lambda item: item.name.casefold()):
            title = path.name[:-3]
            candidates.append(
                {
                    "path": path.relative_to(vault).as_posix(),
                    "title": title,
                    "linked_in": sorted(links.get(title, set())),
                }
            )

    result = {
        "vault": str(vault),
        "missing_index_files": missing,
        "candidate_count": len(candidates),
        "candidates": candidates,
        "multiple_primary_indexes": [
            item for item in candidates if len(item["linked_in"]) > 1
        ],
    }
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Vault: {vault}")
        print(f"Candidates: {len(candidates)}")
        for item in candidates:
            coverage = ", ".join(item["linked_in"]) or "unlinked"
            print(f"- {item['path']} [{coverage}]")
        if missing:
            print("Missing indexes:")
            for path in missing:
                print(f"- {path}")
    return 2 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
