from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Iterable

from rapidfuzz import fuzz, process

from function_search.models import FunctionEntry, SearchResult

DEFAULT_LIMIT = 50


class SearchEngine:
    """Hybrid SQLite FTS5 + rapidfuzz search engine."""

    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        self._conn: sqlite3.Connection | None = None
        self._entries_by_id: dict[str, FunctionEntry] = {}
        self._name_choices: dict[str, str] = {}

    def connect(self) -> None:
        if self._conn is not None:
            return
        uri = f"file:{self.db_path}?mode=ro"
        self._conn = sqlite3.connect(uri, uri=True, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._load_entry_cache()

    def close(self) -> None:
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def _load_entry_cache(self) -> None:
        assert self._conn is not None
        rows = self._conn.execute(
            "SELECT id, provider, category, name, full_name, signature, "
            "description, example, module, tags FROM entries"
        ).fetchall()
        for row in rows:
            tags = json.loads(row["tags"]) if row["tags"] else []
            entry = FunctionEntry(
                id=row["id"],
                provider=row["provider"],
                category=row["category"],
                name=row["name"],
                full_name=row["full_name"],
                signature=row["signature"] or "",
                description=row["description"] or "",
                example=row["example"] or "",
                module=row["module"] or "",
                tags=tags,
            )
            self._entries_by_id[entry.id] = entry
            self._name_choices[entry.full_name] = entry.id
            self._name_choices[entry.name] = entry.id

    @property
    def entry_count(self) -> int:
        self.connect()
        return len(self._entries_by_id)

    @property
    def providers(self) -> list[str]:
        self.connect()
        assert self._conn is not None
        rows = self._conn.execute(
            "SELECT DISTINCT provider FROM entries ORDER BY provider"
        ).fetchall()
        return [row[0] for row in rows]

    def search(
        self,
        query: str,
        *,
        provider: str | None = None,
        limit: int = DEFAULT_LIMIT,
    ) -> list[SearchResult]:
        self.connect()
        query = query.strip()
        if not query:
            return self._browse(provider=provider, limit=limit)

        candidate_ids = self._collect_candidates(query, provider=provider)
        if not candidate_ids:
            return self._fuzzy_fallback(query, provider=provider, limit=limit)

        return self._rank_candidates(query, candidate_ids, limit=limit)

    def get_entry(self, entry_id: str) -> FunctionEntry | None:
        self.connect()
        return self._entries_by_id.get(entry_id)

    def _browse(self, *, provider: str | None, limit: int) -> list[SearchResult]:
        assert self._conn is not None
        if provider:
            rows = self._conn.execute(
                "SELECT id FROM entries WHERE provider = ? ORDER BY name LIMIT ?",
                (provider, limit),
            ).fetchall()
        else:
            rows = self._conn.execute(
                "SELECT id FROM entries ORDER BY provider, name LIMIT ?",
                (limit,),
            ).fetchall()
        results: list[SearchResult] = []
        for row in rows:
            entry = self._entries_by_id[row["id"]]
            results.append(SearchResult(entry=entry, score=0.0, match_reason="browse"))
        return results

    def _collect_candidates(
        self, query: str, *, provider: str | None
    ) -> set[str]:
        assert self._conn is not None
        candidate_ids: set[str] = set()
        like = f"%{query}%"
        provider_clause = ""
        params: list[object] = [like, like, like]

        if provider:
            provider_clause = "AND provider = ?"
            params.append(provider)

        rows = self._conn.execute(
            f"""
            SELECT id FROM entries
            WHERE (name LIKE ? OR full_name LIKE ? OR module LIKE ?)
            {provider_clause}
            LIMIT 200
            """,
            params,
        ).fetchall()
        candidate_ids.update(row["id"] for row in rows)

        fts_query = self._build_fts_query(query)
        if fts_query:
            fts_params: list[object] = [fts_query]
            fts_provider = ""
            if provider:
                fts_provider = "AND e.provider = ?"
                fts_params.append(provider)
            fts_rows = self._conn.execute(
                f"""
                SELECT e.id
                FROM entries_fts fts
                JOIN entries e ON e.rowid = fts.rowid
                WHERE entries_fts MATCH ?
                {fts_provider}
                LIMIT 200
                """,
                fts_params,
            ).fetchall()
            candidate_ids.update(row["id"] for row in fts_rows)

        exact = process.extract(
            query,
            self._name_choices.keys(),
            scorer=fuzz.WRatio,
            limit=30,
        )
        for name, score, _ in exact:
            if score >= 70:
                candidate_ids.add(self._name_choices[name])

        return candidate_ids

    def _fuzzy_fallback(
        self, query: str, *, provider: str | None, limit: int
    ) -> list[SearchResult]:
        choices: dict[str, str] = {}
        for entry in self._entries_by_id.values():
            if provider and entry.provider != provider:
                continue
            choices[entry.full_name] = entry.id
            choices[entry.name] = entry.id

        matches = process.extract(
            query,
            choices.keys(),
            scorer=fuzz.WRatio,
            limit=limit,
        )
        results: list[SearchResult] = []
        seen: set[str] = set()
        for name, score, _ in matches:
            entry_id = choices[name]
            if entry_id in seen:
                continue
            seen.add(entry_id)
            entry = self._entries_by_id[entry_id]
            results.append(
                SearchResult(
                    entry=entry,
                    score=float(score),
                    match_reason="fuzzy",
                )
            )
        return results

    def _rank_candidates(
        self, query: str, candidate_ids: Iterable[str], *, limit: int
    ) -> list[SearchResult]:
        q = query.lower()
        scored: list[SearchResult] = []

        for entry_id in candidate_ids:
            entry = self._entries_by_id.get(entry_id)
            if entry is None:
                continue

            name_l = entry.name.lower()
            full_l = entry.full_name.lower()
            score = 0.0
            reason = "match"

            if name_l == q or full_l == q:
                score = 200.0
                reason = "exact"
            elif name_l.startswith(q) or full_l.startswith(q):
                score = 150.0 + len(q)
                reason = "prefix"
            elif q in name_l or q in full_l:
                score = 120.0
                reason = "substring"
            else:
                name_score = fuzz.WRatio(q, name_l)
                full_score = fuzz.partial_ratio(q, full_l)
                blob_score = fuzz.token_set_ratio(q, entry.search_blob().lower())
                score = max(name_score, full_score, blob_score)
                reason = "fuzzy"

            if q in entry.description.lower():
                score += 10.0
            if any(q in tag.lower() for tag in entry.tags):
                score += 8.0

            scored.append(SearchResult(entry=entry, score=score, match_reason=reason))

        scored.sort(key=lambda r: (-r.score, r.entry.name))
        return scored[:limit]

    @staticmethod
    def _build_fts_query(query: str) -> str:
        tokens = [t for t in query.replace(".", " ").split() if t.strip()]
        if not tokens:
            return ""
        parts = []
        for token in tokens:
            safe = "".join(ch for ch in token if ch.isalnum() or ch in ("_", "-"))
            if safe:
                parts.append(f'"{safe}"*')
        return " AND ".join(parts)


class IndexBuilder:
    """Builds the SQLite search index from provider entries."""

    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path

    def build(self, entries: Iterable[FunctionEntry]) -> int:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        if self.db_path.exists():
            self.db_path.unlink()

        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute("PRAGMA journal_mode=OFF")
            conn.execute("PRAGMA synchronous=OFF")
            self._create_schema(conn)
            count = self._insert_entries(conn, list(entries))
            conn.commit()
            return count
        finally:
            conn.close()

    @staticmethod
    def _create_schema(conn: sqlite3.Connection) -> None:
        conn.executescript(
            """
            CREATE TABLE entries (
                id TEXT PRIMARY KEY,
                provider TEXT NOT NULL,
                category TEXT NOT NULL,
                name TEXT NOT NULL,
                full_name TEXT NOT NULL,
                signature TEXT,
                description TEXT,
                example TEXT,
                module TEXT,
                tags TEXT,
                search_blob TEXT
            );

            CREATE INDEX idx_entries_provider ON entries(provider);
            CREATE INDEX idx_entries_name ON entries(name);
            CREATE INDEX idx_entries_full_name ON entries(full_name);

            CREATE VIRTUAL TABLE entries_fts USING fts5(
                name,
                full_name,
                category,
                module,
                signature,
                description,
                tags,
                content='entries',
                content_rowid='rowid'
            );

            CREATE TRIGGER entries_ai AFTER INSERT ON entries BEGIN
                INSERT INTO entries_fts(
                    rowid, name, full_name, category, module, signature, description, tags
                ) VALUES (
                    new.rowid, new.name, new.full_name, new.category, new.module,
                    new.signature, new.description, new.tags
                );
            END;

            CREATE TRIGGER entries_ad AFTER DELETE ON entries BEGIN
                INSERT INTO entries_fts(entries_fts, rowid, name, full_name, category, module, signature, description, tags)
                VALUES('delete', old.rowid, old.name, old.full_name, old.category, old.module, old.signature, old.description, old.tags);
            END;

            CREATE TRIGGER entries_au AFTER UPDATE ON entries BEGIN
                INSERT INTO entries_fts(entries_fts, rowid, name, full_name, category, module, signature, description, tags)
                VALUES('delete', old.rowid, old.name, old.full_name, old.category, old.module, old.signature, old.description, old.tags);
                INSERT INTO entries_fts(
                    rowid, name, full_name, category, module, signature, description, tags
                ) VALUES (
                    new.rowid, new.name, new.full_name, new.category, new.module,
                    new.signature, new.description, new.tags
                );
            END;
            """
        )

    @staticmethod
    def _insert_entries(conn: sqlite3.Connection, entries: list[FunctionEntry]) -> int:
        rows = []
        for entry in entries:
            rows.append(
                (
                    entry.id,
                    entry.provider,
                    entry.category,
                    entry.name,
                    entry.full_name,
                    entry.signature,
                    entry.description,
                    entry.example,
                    entry.module,
                    json.dumps(entry.tags, ensure_ascii=False),
                    entry.search_blob(),
                )
            )
        conn.executemany(
            """
            INSERT INTO entries (
                id, provider, category, name, full_name, signature,
                description, example, module, tags, search_blob
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            rows,
        )
        conn.execute("INSERT INTO entries_fts(entries_fts) VALUES('rebuild')")
        return len(rows)
