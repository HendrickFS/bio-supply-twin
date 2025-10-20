"""
Bio Supply Digital Twin Service - Database Manager
=================================================

Purpose:
    Async database manager for accessing the Django database from the
    digital twin service. Uses PostgreSQL when DATABASE_URL points to
    Postgres (docker-compose), and falls back to SQLite for local/dev.

Key Features:
    - Async PostgreSQL operations using asyncpg
    - Async SQLite operations using aiosqlite (fallback)
    - Read access to Django ORM-generated tables
    - Error handling and logging for database operations
    - Efficient data retrieval with proper SQL joins

Tables (Django defaults):
    - core_transportbox
    - core_sample
    - core_telemetryreading
    - core_slaconfig
    - core_alert
"""

import os
import asyncio
import logging
import aiosqlite
import asyncpg

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        # Prefer DATABASE_URL if provided (compose sets Postgres URL)
        self.database_url = os.getenv('DATABASE_URL')
        self.use_postgres = bool(self.database_url and self.database_url.startswith("postgres"))
        self.db_path = '../db.sqlite3'
        self._pg_pool: asyncpg.Pool | None = None

    async def _get_pool(self) -> asyncpg.Pool:
        """Get or create a Postgres connection pool."""
        if self._pg_pool is None:
            if not self.use_postgres:
                raise RuntimeError("Postgres pool requested but use_postgres=False")
            # Minimum reasonable pool size for a small service
            self._pg_pool = await asyncpg.create_pool(self.database_url, min_size=1, max_size=5)
        return self._pg_pool
    
    async def get_all_samples(self):
        """Fetch all samples with joined box info (returns sample-centric fields)."""
        try:
            if self.use_postgres:
                pool = await self._get_pool()
                async with pool.acquire() as con:
                    rows = await con.fetch(
                        """
                        SELECT s.sample_id, b.box_id AS box_ext_id, s.name, s.description, s.collected_at,
                               s.status, s.temperature, s.humidity, s.last_updated
                        FROM core_sample s
                        JOIN core_transportbox b ON s.box_id = b.id
                        ORDER BY s.id DESC
                        """
                    )
                    return [
                        {
                            'sample_id': r['sample_id'],
                            'box_id': r['box_ext_id'],
                            'name': r['name'],
                            'description': r['description'],
                            'collected_at': r['collected_at'],
                            'status': r['status'],
                            'temperature': r['temperature'],
                            'humidity': r['humidity'],
                            'last_updated': r['last_updated'],
                        } for r in rows
                    ]
            else:
                async with aiosqlite.connect(self.db_path) as db:
                    query = (
                        "SELECT s.sample_id, b.box_id AS box_ext_id, s.name, s.description, s.collected_at, "
                        "s.status, s.temperature, s.humidity, s.last_updated "
                        "FROM core_sample s JOIN core_transportbox b ON s.box_id = b.id ORDER BY s.id DESC"
                    )
                    async with db.execute(query) as cursor:
                        rows = await cursor.fetchall()
                        return [
                            {
                                'sample_id': r[0], 'box_id': r[1], 'name': r[2], 'description': r[3],
                                'collected_at': r[4], 'status': r[5], 'temperature': r[6], 'humidity': r[7],
                                'last_updated': r[8]
                            } for r in rows
                        ]
        except Exception as e:
            print(f"Error fetching samples: {e}")
            return []

    async def get_sample(self, sample_id):
        """Fetch a sample by its sample_id string."""
        try:
            if self.use_postgres:
                pool = await self._get_pool()
                async with pool.acquire() as con:
                    row = await con.fetchrow(
                        """
                        SELECT s.sample_id, b.box_id AS box_ext_id, s.name, s.description, s.collected_at,
                               s.status, s.temperature, s.humidity, s.last_updated
                        FROM core_sample s JOIN core_transportbox b ON s.box_id = b.id
                        WHERE s.sample_id = $1
                        """,
                        sample_id,
                    )
                    if row:
                        return {
                            'sample_id': row['sample_id'], 'box_id': row['box_ext_id'], 'name': row['name'],
                            'description': row['description'], 'collected_at': row['collected_at'],
                            'status': row['status'], 'temperature': row['temperature'], 'humidity': row['humidity'],
                            'last_updated': row['last_updated'],
                        }
                    return None
            else:
                async with aiosqlite.connect(self.db_path) as db:
                    query = (
                        "SELECT s.sample_id, b.box_id AS box_ext_id, s.name, s.description, s.collected_at, "
                        "s.status, s.temperature, s.humidity, s.last_updated "
                        "FROM core_sample s JOIN core_transportbox b ON s.box_id = b.id WHERE s.sample_id = ?"
                    )
                    async with db.execute(query, (sample_id,)) as cursor:
                        r = await cursor.fetchone()
                        if r:
                            return {
                                'sample_id': r[0], 'box_id': r[1], 'name': r[2], 'description': r[3],
                                'collected_at': r[4], 'status': r[5], 'temperature': r[6], 'humidity': r[7],
                                'last_updated': r[8]
                            }
                        return None
        except Exception as e:
            print(f"Error fetching sample {sample_id}: {e}")
            return None
        
    async def sample_count(self):
        """Get the total count of samples."""
        try:
            if self.use_postgres:
                pool = await self._get_pool()
                async with pool.acquire() as con:
                    row = await con.fetchval("SELECT COUNT(*) FROM core_sample")
                    return int(row or 0)
            else:
                async with aiosqlite.connect(self.db_path) as db:
                    query = "SELECT COUNT(*) FROM core_sample"
                    async with db.execute(query) as cursor:
                        row = await cursor.fetchone()
                        return row[0] if row else 0
        except Exception as e:
            print(f"Error counting samples: {e}")
            return 0
        
    async def get_all_boxes(self):
        """Fetch all transport boxes from the database."""
        try:
            if self.use_postgres:
                pool = await self._get_pool()
                async with pool.acquire() as con:
                    rows = await con.fetch(
                        """
                        SELECT box_id, geolocation, temperature, humidity, last_updated, status
                        FROM core_transportbox
                        ORDER BY id DESC
                        """
                    )
                    return [
                        {
                            'box_id': r['box_id'], 'geolocation': r['geolocation'], 'temperature': r['temperature'],
                            'humidity': r['humidity'], 'last_updated': r['last_updated'], 'status': r['status']
                        } for r in rows
                    ]
            else:
                async with aiosqlite.connect(self.db_path) as db:
                    query = (
                        "SELECT box_id, geolocation, temperature, humidity, last_updated, status "
                        "FROM core_transportbox ORDER BY id DESC"
                    )
                    async with db.execute(query) as cursor:
                        rows = await cursor.fetchall()
                        return [
                            {
                                'box_id': r[0], 'geolocation': r[1], 'temperature': r[2], 'humidity': r[3],
                                'last_updated': r[4], 'status': r[5]
                            } for r in rows
                        ]
        except Exception as e:
            print(f"Error fetching boxes: {e}")
            return []
        
    async def get_box(self, box_id):
        """Fetch a transport box by its box_id string."""
        try:
            if self.use_postgres:
                pool = await self._get_pool()
                async with pool.acquire() as con:
                    row = await con.fetchrow(
                        """
                        SELECT box_id, geolocation, temperature, humidity, last_updated, status
                        FROM core_transportbox WHERE box_id = $1
                        """,
                        box_id,
                    )
                    if row:
                        return {
                            'box_id': row['box_id'], 'geolocation': row['geolocation'], 'temperature': row['temperature'],
                            'humidity': row['humidity'], 'last_updated': row['last_updated'], 'status': row['status']
                        }
                    return None
            else:
                async with aiosqlite.connect(self.db_path) as db:
                    query = (
                        "SELECT box_id, geolocation, temperature, humidity, last_updated, status "
                        "FROM core_transportbox WHERE box_id = ?"
                    )
                    async with db.execute(query, (box_id,)) as cursor:
                        r = await cursor.fetchone()
                        if r:
                            return {
                                'box_id': r[0], 'geolocation': r[1], 'temperature': r[2], 'humidity': r[3],
                                'last_updated': r[4], 'status': r[5]
                            }
                        return None
        except Exception as e:
            print(f"Error fetching box {box_id}: {e}")
            return None

    async def box_count(self):
        """Get the total count of transport boxes."""
        try:
            if self.use_postgres:
                pool = await self._get_pool()
                async with pool.acquire() as con:
                    row = await con.fetchval("SELECT COUNT(*) FROM core_transportbox")
                    return int(row or 0)
            else:
                async with aiosqlite.connect(self.db_path) as db:
                    query = "SELECT COUNT(*) FROM core_transportbox"
                    async with db.execute(query) as cursor:
                        row = await cursor.fetchone()
                        return row[0] if row else 0
        except Exception as e:
            print(f"Error counting boxes: {e}")
            return 0

    async def active_alert_count(self):
        try:
            if self.use_postgres:
                pool = await self._get_pool()
                async with pool.acquire() as con:
                    row = await con.fetchval("SELECT COUNT(*) FROM core_alert WHERE is_active = TRUE")
                    return int(row or 0)
            else:
                async with aiosqlite.connect(self.db_path) as db:
                    query = "SELECT COUNT(*) FROM core_alert WHERE is_active = 1"
                    async with db.execute(query) as cursor:
                        row = await cursor.fetchone()
                        return row[0] if row else 0
        except Exception as e:
            print(f"Error counting active alerts: {e}")
            return 0

    async def list_telemetry(self, box_id: int = None, sample_id: int = None, since_iso: str = None):
        try:
            if self.use_postgres:
                pool = await self._get_pool()
                async with pool.acquire() as con:
                    clauses = []
                    params = []
                    if box_id is not None:
                        clauses.append("box_id = $%d" % (len(params) + 1))
                        params.append(box_id)
                    if sample_id is not None:
                        clauses.append("sample_id = $%d" % (len(params) + 1))
                        params.append(sample_id)
                    if since_iso is not None:
                        clauses.append("timestamp >= $%d" % (len(params) + 1))
                        params.append(since_iso)
                    where = (" WHERE " + " AND ".join(clauses)) if clauses else ""
                    query = (
                        "SELECT id, box_id, sample_id, timestamp, temperature, humidity, geolocation "
                        "FROM core_telemetryreading" + where + " ORDER BY timestamp DESC LIMIT 1000"
                    )
                    rows = await con.fetch(query, *params)
                    return [
                        {
                            'id': r['id'], 'box': r['box_id'], 'sample': r['sample_id'], 'timestamp': r['timestamp'],
                            'temperature': r['temperature'], 'humidity': r['humidity'], 'geolocation': r['geolocation']
                        } for r in rows
                    ]
            else:
                async with aiosqlite.connect(self.db_path) as db:
                    base = "SELECT id, box_id, sample_id, timestamp, temperature, humidity, geolocation FROM core_telemetryreading"
                    clauses = []
                    params = []
                    if box_id is not None:
                        clauses.append("box_id = ?")
                        params.append(box_id)
                    if sample_id is not None:
                        clauses.append("sample_id = ?")
                        params.append(sample_id)
                    if since_iso is not None:
                        clauses.append("timestamp >= ?")
                        params.append(since_iso)
                    where = (" WHERE " + " AND ".join(clauses)) if clauses else ""
                    order = " ORDER BY timestamp DESC LIMIT 1000"
                    query = base + where + order
                    async with db.execute(query, params) as cursor:
                        rows = await cursor.fetchall()
                        return [
                            {
                                'id': r[0], 'box': r[1], 'sample': r[2], 'timestamp': r[3],
                                'temperature': r[4], 'humidity': r[5], 'geolocation': r[6]
                            } for r in rows
                        ]
        except Exception as e:
            print(f"Error listing telemetry: {e}")
            return []

    async def create_sla(self, name: str, temp_min: float, temp_max: float, humidity_min: float, humidity_max: float):
        try:
            if self.use_postgres:
                pool = await self._get_pool()
                async with pool.acquire() as con:
                    await con.execute(
                        """
                        INSERT INTO core_slaconfig (name, temp_min, temp_max, humidity_min, humidity_max, created_at, updated_at)
                        VALUES ($1, $2, $3, $4, $5, NOW(), NOW())
                        """,
                        name, temp_min, temp_max, humidity_min, humidity_max,
                    )
                    return True
            else:
                async with aiosqlite.connect(self.db_path) as db:
                    await db.execute(
                        "INSERT INTO core_slaconfig (name, temp_min, temp_max, humidity_min, humidity_max, created_at, updated_at) VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)",
                        (name, temp_min, temp_max, humidity_min, humidity_max),
                    )
                    await db.commit()
                    return True
        except Exception as e:
            print(f"Error creating SLA: {e}")
            return False

    async def list_sla(self):
        try:
            if self.use_postgres:
                pool = await self._get_pool()
                async with pool.acquire() as con:
                    rows = await con.fetch(
                        "SELECT id, name, temp_min, temp_max, humidity_min, humidity_max, created_at, updated_at FROM core_slaconfig ORDER BY id DESC"
                    )
                    return [
                        {
                            'id': r['id'], 'name': r['name'], 'temp_min': r['temp_min'], 'temp_max': r['temp_max'],
                            'humidity_min': r['humidity_min'], 'humidity_max': r['humidity_max'],
                            'created_at': r['created_at'], 'updated_at': r['updated_at']
                        } for r in rows
                    ]
            else:
                async with aiosqlite.connect(self.db_path) as db:
                    query = "SELECT id, name, temp_min, temp_max, humidity_min, humidity_max, created_at, updated_at FROM core_slaconfig ORDER BY id DESC"
                    async with db.execute(query) as cursor:
                        rows = await cursor.fetchall()
                        return [
                            {
                                'id': r[0], 'name': r[1], 'temp_min': r[2], 'temp_max': r[3],
                                'humidity_min': r[4], 'humidity_max': r[5], 'created_at': r[6], 'updated_at': r[7]
                            } for r in rows
                        ]
        except Exception as e:
            print(f"Error listing SLA: {e}")
            return []

    async def create_alert(self, payload: dict):
        try:
            if self.use_postgres:
                pool = await self._get_pool()
                async with pool.acquire() as con:
                    await con.execute(
                        """
                        INSERT INTO core_alert (box_id, sample_id, type, severity, message, started_at, last_seen_at, resolved_at, acknowledged_at, is_active)
                        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
                        """,
                        payload.get('box'), payload.get('sample'), payload['type'], payload['severity'], payload.get('message', ''),
                        payload['started_at'], payload['last_seen_at'], payload.get('resolved_at'), payload.get('acknowledged_at'), True if payload.get('is_active', True) else False
                    )
                    return True
            else:
                async with aiosqlite.connect(self.db_path) as db:
                    await db.execute(
                        "INSERT INTO core_alert (box_id, sample_id, type, severity, message, started_at, last_seen_at, resolved_at, acknowledged_at, is_active) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (
                            payload.get('box'), payload.get('sample'), payload['type'], payload['severity'], payload.get('message', ''),
                            payload['started_at'], payload['last_seen_at'], payload.get('resolved_at'), payload.get('acknowledged_at'), 1 if payload.get('is_active', True) else 0
                        ),
                    )
                    await db.commit()
                    return True
        except Exception as e:
            print(f"Error creating alert: {e}")
            return False

    async def list_alerts(self, active_only: bool = False):
        try:
            if self.use_postgres:
                pool = await self._get_pool()
                async with pool.acquire() as con:
                    where = " WHERE is_active = TRUE" if active_only else ""
                    query = (
                        "SELECT id, box_id, sample_id, type, severity, message, started_at, last_seen_at, resolved_at, acknowledged_at, is_active "
                        "FROM core_alert" + where + " ORDER BY started_at DESC"
                    )
                    rows = await con.fetch(query)
                    return [
                        {
                            'id': r['id'], 'box': r['box_id'], 'sample': r['sample_id'], 'type': r['type'], 'severity': r['severity'],
                            'message': r['message'], 'started_at': r['started_at'], 'last_seen_at': r['last_seen_at'],
                            'resolved_at': r['resolved_at'], 'acknowledged_at': r['acknowledged_at'], 'is_active': bool(r['is_active'])
                        } for r in rows
                    ]
            else:
                async with aiosqlite.connect(self.db_path) as db:
                    base = "SELECT id, box_id, sample_id, type, severity, message, started_at, last_seen_at, resolved_at, acknowledged_at, is_active FROM core_alert"
                    where = " WHERE is_active = 1" if active_only else ""
                    order = " ORDER BY started_at DESC"
                    query = base + where + order
                    async with db.execute(query) as cursor:
                        rows = await cursor.fetchall()
                        return [
                            {
                                'id': r[0], 'box': r[1], 'sample': r[2], 'type': r[3], 'severity': r[4], 'message': r[5],
                                'started_at': r[6], 'last_seen_at': r[7], 'resolved_at': r[8], 'acknowledged_at': r[9], 'is_active': bool(r[10])
                            } for r in rows
                        ]
        except Exception as e:
            print(f"Error listing alerts: {e}")
            return []