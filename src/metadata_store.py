import sqlite3
from typing import Dict, List, Tuple, Optional

class MetadataStore:
    def __init__(self, db_path: str = "surgical_metadata.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self._init_schema()

    def _init_schema(self) -> None:
        cur = self.conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS surgical_index (
            image_id TEXT PRIMARY KEY,
            s3_uri TEXT NOT NULL,
            anatomy TEXT NOT NULL,
            view_type TEXT NOT NULL,
            pelvic_tilt REAL NOT NULL,
            noise_sigma REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        self.conn.commit()

    def insert(self, record: Dict) -> None:
        cur = self.conn.cursor()
        cur.execute("""
        INSERT OR REPLACE INTO surgical_index
        (image_id, s3_uri, anatomy, view_type, pelvic_tilt, noise_sigma)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            record["image_id"],
            record["s3_uri"],
            record["anatomy"],
            record["view_type"],
            float(record["pelvic_tilt"]),
            float(record["noise_sigma"]),
        ))
        self.conn.commit()

    def query(self, anatomy: str = "Hip", min_tilt: Optional[float] = None) -> List[Tuple]:
        cur = self.conn.cursor()
        q = "SELECT image_id, pelvic_tilt, s3_uri FROM surgical_index WHERE anatomy=?"
        params = [anatomy]
        if min_tilt is not None:
            q += " AND pelvic_tilt > ?"
            params.append(float(min_tilt))
        return cur.execute(q, tuple(params)).fetchall()

