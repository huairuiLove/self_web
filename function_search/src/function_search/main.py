from __future__ import annotations

import argparse
import sys
from pathlib import Path

from function_search.build_index import build_index
from function_search.paths import default_db_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Function Search - PyTorch / Python / Backend API lookup"
    )
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("gui", help="Launch desktop search app (default)")

    build_parser = sub.add_parser("build", help="Build search index")
    build_parser.add_argument("--output", type=Path, default=None)
    build_parser.add_argument("--no-pytorch", action="store_true")

    search_parser = sub.add_parser("search", help="Search from command line")
    search_parser.add_argument("query", nargs="+", help="Search query")
    search_parser.add_argument("--provider", default=None)
    search_parser.add_argument("--limit", type=int, default=10)

    ask_parser = sub.add_parser("ask", help="Ask LM Studio code assistant")
    ask_parser.add_argument("question", nargs="+", help="Question to ask")
    ask_parser.add_argument("--provider", default=None)

    args = parser.parse_args()
    command = args.command or "gui"

    if command == "build":
        out = args.output or default_db_path()
        build_index(out, include_pytorch=not args.no_pytorch)
        return

    if command == "search":
        from function_search.search_engine import SearchEngine

        db = default_db_path()
        if not db.exists():
            print(f"Index not found: {db}. Run: function-search build", file=sys.stderr)
            sys.exit(1)
        engine = SearchEngine(db)
        engine.connect()
        query = " ".join(args.query)
        results = engine.search(query, provider=args.provider, limit=args.limit)
        for i, result in enumerate(results, 1):
            entry = result.entry
            print(f"{i}. [{entry.provider}] {entry.full_name} (score={result.score:.0f})")
            if entry.description:
                print(f"   {entry.description[:120]}")
        engine.close()
        return

    if command == "ask":
        from function_search.config import AppConfig
        from function_search.lm_studio_client import LMStudioError
        from function_search.qa_assistant import QAAssistant
        from function_search.search_engine import SearchEngine

        db = default_db_path()
        if not db.exists():
            print(f"Index not found: {db}. Run: function-search build", file=sys.stderr)
            sys.exit(1)

        engine = SearchEngine(db)
        engine.connect()
        assistant = QAAssistant(engine, AppConfig.load())
        question = " ".join(args.question)

        try:
            result = assistant.answer(question, provider=args.provider)
        except LMStudioError as exc:
            print(str(exc), file=sys.stderr)
            sys.exit(1)
        finally:
            engine.close()

        if result.context_entries:
            print("--- 检索上下文 ---")
            for item in result.context_entries[:5]:
                print(f"- {item.entry.full_name}")
            print()

        print(result.answer)
        return

    from function_search.app import run_app

    run_app()


if __name__ == "__main__":
    main()
