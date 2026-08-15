#!/usr/bin/env python3
"""Find exact or similar Markdown filenames under a Vault's pages-ai tree."""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path


def normalized_name(value: str) -> str:
    name = Path(value.strip()).name
    if name.casefold().endswith(".md"):
        name = name[:-3]
    name = unicodedata.normalize("NFKC", name).casefold()
    return re.sub(r"[\s\-_—–·・:：,，.。()（）\[\]【】《》〈〉]+", "", name)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vault", required=True, type=Path)
    parser.add_argument("--name", required=True)
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    pages_ai = args.vault.expanduser().resolve() / "pages-ai"
    if not pages_ai.is_dir():
        parser.error(f"pages-ai directory not found: {pages_ai}")

    query = normalized_name(args.name)
    candidates = []
    for path in sorted(pages_ai.rglob("*.md")):
        if path.name.endswith("-去掉AI味.md") and not args.name.rstrip().removesuffix(".md").endswith("-去掉AI味"):
            continue
        candidate = normalized_name(path.name)
        score = SequenceMatcher(None, query, candidate).ratio() if query or candidate else 1.0
        candidates.append(
            {
                "path": path.relative_to(args.vault.resolve()).as_posix(),
                "name": path.name,
                "score": round(score, 4),
                "exact": candidate == query,
            }
        )

    exact = [item for item in candidates if item["exact"]]
    similar = sorted(
        (item for item in candidates if not item["exact"] and item["score"] >= 0.45),
        key=lambda item: (-item["score"], item["path"]),
    )[: max(args.limit, 0)]
    result = {"query": args.name, "exact": exact, "similar": similar}

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for label in ("exact", "similar"):
            for item in result[label]:
                print(f"{label}\t{item['score']:.4f}\t{item['path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
