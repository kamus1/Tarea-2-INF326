import sqlite3
from typing import Optional

from .config import DB_PATH, INITIAL_ID


# se inicializa la base de datos
def init_db():
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hash TEXT UNIQUE NOT NULL,
                long_url TEXT NOT NULL
            );
            """
        )
        conn.commit()

        # asegurar que el autoincremento comience desde INITIAL_ID
        cur.execute("SELECT COUNT(*) FROM urls;")
        count = cur.fetchone()[0]
        if count == 0:
            cur.execute("DELETE FROM sqlite_sequence WHERE name='urls';")
            cur.execute(
                "INSERT INTO sqlite_sequence (name, seq) VALUES ('urls', ?);",
                (INITIAL_ID - 1,),
            )
            conn.commit()

    finally:
        conn.close()


def insert_placeholder(long_url: str) -> int:
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO urls (hash, long_url) VALUES (?, ?);",
            ("__temp__", long_url),
        )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def update_hash_for_id(row_id: int, hash_str: str) -> None:
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        cur.execute("UPDATE urls SET hash=? WHERE id=?;", (hash_str, row_id))
        conn.commit()
    finally:
        conn.close()


def get_long_url(hash_str: str) -> Optional[str]:
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        cur.execute("SELECT long_url FROM urls WHERE hash = ?;", (hash_str,))
        row = cur.fetchone()
        return row[0] if row else None
    finally:
        conn.close()


def url_exists(long_url: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM urls WHERE long_url = ? LIMIT 1;", (long_url,))
        row = cur.fetchone()
        return bool(row)
    finally:
        conn.close()
