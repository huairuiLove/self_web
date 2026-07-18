from __future__ import annotations

import tempfile
from pathlib import Path

from function_search.models import FunctionEntry
from function_search.providers.json_provider import JsonDataProvider
from function_search.search_engine import IndexBuilder, SearchEngine


def _data_dir() -> Path:
    return Path(__file__).resolve().parents[1] / "src" / "function_search" / "data"


def _sample_entries() -> list[FunctionEntry]:
    provider = JsonDataProvider(
        "python",
        "Python",
        _data_dir() / "python_common.json",
    )
    return provider.collect()


def test_index_and_exact_search() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        db = Path(tmp) / "test.db"
        entries = _sample_entries()
        count = IndexBuilder(db).build(entries)
        assert count == len(entries)

        engine = SearchEngine(db)
        engine.connect()

        results = engine.search("json.dumps")
        assert results
        assert results[0].entry.full_name == "json.dumps"
        assert results[0].score >= 150

        results = engine.search("print")
        assert any(r.entry.name == "print" for r in results)

        engine.close()


def test_fuzzy_search() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        db = Path(tmp) / "test.db"
        IndexBuilder(db).build(_sample_entries())
        engine = SearchEngine(db)
        engine.connect()

        results = engine.search("json dump")
        assert results
        assert results[0].entry.full_name == "json.dumps"

        engine.close()


def test_provider_filter() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        db = Path(tmp) / "test.db"
        backend = JsonDataProvider(
            "backend",
            "Backend",
            _data_dir() / "backend_common.json",
        )
        python = JsonDataProvider(
            "python",
            "Python",
            _data_dir() / "python_common.json",
        )
        IndexBuilder(db).build(backend.collect() + python.collect())

        engine = SearchEngine(db)
        engine.connect()
        results = engine.search("FastAPI", provider="backend")
        assert results
        assert all(r.entry.provider == "backend" for r in results)
        engine.close()
