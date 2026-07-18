from __future__ import annotations

import argparse
import json
from pathlib import Path

from function_search.paths import default_db_path, package_root
from function_search.providers.registry import get_all_providers
from function_search.search_engine import IndexBuilder


def _load_extension_providers(extensions_dir: Path):
    from function_search.extensions_loader import load_extension_providers

    return load_extension_providers(extensions_dir)


def build_index(
    db_path: Path | None = None,
    *,
    include_pytorch: bool = True,
    extensions_dir: Path | None = None,
    export_json: Path | None = None,
) -> int:
    db_path = db_path or default_db_path()
    providers = get_all_providers(include_pytorch=include_pytorch)

    ext_dir = extensions_dir
    if ext_dir is None:
        project_root = package_root().parent.parent
        candidate = project_root / "extensions"
        if candidate.exists():
            ext_dir = candidate

    if ext_dir and ext_dir.exists():
        ext_providers = _load_extension_providers(ext_dir)
        providers.extend(ext_providers)
        if ext_providers:
            print(f"  [extensions] {len(ext_providers)} custom provider(s) from {ext_dir}")

    all_entries = []
    stats: dict[str, int] = {}
    for provider in providers:
        entries = provider.collect()
        stats[provider.id] = len(entries)
        all_entries.extend(entries)
        print(f"  [{provider.display_name}] {len(entries)} entries")

    count = IndexBuilder(db_path).build(all_entries)
    print(f"Built index: {db_path} ({count} total entries)")

    if export_json:
        export_json.parent.mkdir(parents=True, exist_ok=True)
        payload = [e.to_dict() for e in all_entries]
        export_json.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"Exported JSON: {export_json}")

    return count


def main() -> None:
    parser = argparse.ArgumentParser(description="Build function search index")
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output SQLite database path (default: package data/functions.db)",
    )
    parser.add_argument(
        "--no-pytorch",
        action="store_true",
        help="Skip PyTorch introspection (Python + backend only)",
    )
    parser.add_argument(
        "--export-json",
        type=Path,
        default=None,
        help="Also export all entries to JSON",
    )
    args = parser.parse_args()

    out = args.output or (package_root() / "data" / "functions.db")
    print("Collecting entries...")
    try:
        build_index(
            out,
            include_pytorch=not args.no_pytorch,
            export_json=args.export_json,
        )
    except RuntimeError as exc:
        if args.no_pytorch:
            raise
        print(f"Warning: {exc}")
        print("Falling back to Python + backend datasets only...")
        build_index(
            out,
            include_pytorch=False,
            export_json=args.export_json,
        )


if __name__ == "__main__":
    main()
