"""
Bio Supply Digital Twin Service - Database Manager
=================================================

Purpose:
    Async database manager for accessing Django SQLite database from the
    digital twin service. Provides read-only access to biological samples
    and transport box data with optimal performance.

Key Features:
    - Async SQLite operations using aiosqlite
    - Read access to Django ORM-generated tables
    - Error handling and logging for database operations
    - Efficient data retrieval with proper SQL joins
    - Type-safe data structures and return values

Database Tables:
    - core_sample: Biological sample records
    - core_transportbox: Transport container records
    - Relationships: sample.box_id -> transportbox.id

Methods:
    - get_sample(sample_id): Retrieve specific sample with box info
    - get_box(box_id): Retrieve specific transport box
    - get_all_samples(): Retrieve all samples with basic info
    - get_all_boxes(): Retrieve all transport boxes with basic info
    - get_sample_count(): Get total count of samples
    - get_box_count(): Get total count of transport boxes

Database Path: ../db.sqlite3 (Django SQLite database)
Dependencies: aiosqlite for async database operations

"""

import aiosqlite

class DatabaseManager:
    def __init__(self):
        self.db_path = '../db.sqlite3'
    
    async def get_all_samples(self):
        """Fetch all samples from the database."""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                query = "SELECT * FROM core_sample JOIN core_transportbox ON core_sample.box_id = core_transportbox.id"
                async with db.execute(query) as cursor:
                    rows = await cursor.fetchall()
                    samples = []
                    for row in rows:
                        samples.append({
                            'sample_id': row[1],
                            'box_id': row[2],
                            'name': row[3],
                            'description': row[4],
                            'collected_at': row[5],
                            'status': row[6],
                            'temperature': row[7],
                            'humidity': row[8],
                            'last_updated': row[9],
                        })
                    return samples
        except Exception as e:
            print(f"Error fetching samples: {e}")
            return []

    async def get_sample(self, sample_id):
        """Fetch a sample by its ID."""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                query = "SELECT * FROM core_sample JOIN core_transportbox ON core_sample.box_id = core_transportbox.id WHERE core_sample.sample_id = ?"
                async with db.execute(query, (sample_id,)) as cursor:
                    row = await cursor.fetchone()
                    if row:
                        return {
                            'sample_id': row[1],
                            'box_id': row[2],
                            'name': row[3],
                            'description': row[4],
                            'collected_at': row[5],
                            'status': row[6],
                            'temperature': row[7],
                            'humidity': row[8],
                            'last_updated': row[9],
                        }
                    return None
        except Exception as e:
            print(f"Error fetching sample {sample_id}: {e}")
            return None
        
    async def sample_count(self):
        """Get the total count of samples."""
        try:
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
            async with aiosqlite.connect(self.db_path) as db:
                query = "SELECT * FROM core_transportbox"
                async with db.execute(query) as cursor:
                    rows = await cursor.fetchall()
                    boxes = []
                    for row in rows:
                        boxes.append({
                            'box_id': row[1],
                            'geolocation': row[2],
                            'temperature': row[3],
                            'humidity': row[4],
                            'last_updated': row[5],
                            'status': row[6],
                        })
                    return boxes
        except Exception as e:
            print(f"Error fetching boxes: {e}")
            return []
        
    async def get_box(self, box_id):
        """Fetch a transport box by its ID."""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                query = "SELECT * FROM core_transportbox WHERE box_id = ?"
                async with db.execute(query, (box_id,)) as cursor:
                    row = await cursor.fetchone()
                    if row:
                        return {
                            'box_id': row[1],
                            'geolocation': row[2],
                            'temperature': row[3],
                            'humidity': row[4],
                            'last_updated': row[5],
                            'status': row[6],
                        }
                    return None
        except Exception as e:
            print(f"Error fetching box {box_id}: {e}")
            return None

    async def box_count(self):
        """Get the total count of transport boxes."""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                query = "SELECT COUNT(*) FROM core_transportbox"
                async with db.execute(query) as cursor:
                    row = await cursor.fetchone()
                    return row[0] if row else 0
        except Exception as e:
            print(f"Error counting boxes: {e}")
            return 0