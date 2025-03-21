"""
Sub_database Module

This module provides a DatabaseHandler class for interacting with an SQLite database.
It includes functionality to build a database, store and retrieve corrections,
and perform database health checks. It also handles law summary operations.

Classes:
    DatabaseHandler: Manages database operations including law summaries.
"""

import asyncio
import aiosqlite
import logging

class DatabaseHandler:
    """
    Manages database operations using aiosqlite, including law summaries.

    Attributes:
        db_path (str): Path to the SQLite database file.
    """

    def __init__(self, db_path):
        """
        Initializes the DatabaseHandler with the database file path.

        Args:
            db_path (str): Path to the SQLite database file.
        """
        self.db_path = db_path

    async def build_database(self):
        """
        Builds the database if it doesn't exist and creates necessary tables.
        """
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("""
                    CREATE TABLE IF NOT EXISTS corrections (
                        situation_id TEXT PRIMARY KEY,
                        correction TEXT,
                        authorized_user TEXT
                    )
                """)
                await db.execute("""
                    CREATE TABLE IF NOT EXISTS law_summaries (
                        law_id TEXT PRIMARY KEY,
                        summary TEXT
                    )
                """)
                await db.commit()
            logging.info("Database built or verified successfully.")
        except Exception as e:
            logging.error(f"Error building database: {e}")

    async def store_correction(self, situation_id, correction, authorized_user):
        """
        Stores a correction in the database.

        Args:
            situation_id (str): ID of the situation.
            correction (str): The correction to store.
            authorized_user (str): User who authorized the correction.
        """
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("""
                    INSERT OR REPLACE INTO corrections (situation_id, correction, authorized_user)
                    VALUES (?, ?, ?)
                """, (situation_id, correction, authorized_user))
                await db.commit()
            logging.info(f"Correction stored for situation ID: {situation_id}")
        except Exception as e:
            logging.error(f"Error storing correction: {e}")

    async def get_stored_correction(self, situation_id):
        """
        Retrieves a stored correction from the database.

        Args:
            situation_id (str): ID of the situation.

        Returns:
            str: The stored correction, or None if not found.
        """
        try:
            async with aiosqlite.connect(self.db_path) as db:
                async with db.execute("""
                    SELECT correction FROM corrections WHERE situation_id = ?
                """, (situation_id,)) as cursor:
                    row = await cursor.fetchone()
                    if row:
                        return row[0]
                    else:
                        return None
        except Exception as e:
            logging.error(f"Error retrieving correction: {e}")
            return None

    async def check_database_health(self, duration_histogram, error_counter):
        """
        Checks the health of the database by executing a simple query.

        Args:
            duration_histogram (Histogram): Prometheus Histogram to track query duration.
            error_counter (Counter): Prometheus Counter to track database errors.
        """
        start_time = asyncio.get_event_loop().time()
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("SELECT 1")
            duration = asyncio.get_event_loop().time() - start_time
            duration_histogram.observe(duration)
            logging.info(f"Database health check successful. Duration: {duration} seconds")
        except Exception as e:
            error_counter.inc()
            logging.error(f"Database health check failed: {e}")
            raise

    async def store_law_summary(self, law_id, summary):
        """
        Stores a law summary in the database.

        Args:
            law_id (str): ID of the law.
            summary (str): The summary of the law.
        """
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("""
                    INSERT OR REPLACE INTO law_summaries (law_id, summary)
                    VALUES (?, ?)
                """, (law_id, summary))
                await db.commit()
            logging.info(f"Law summary stored for law ID: {law_id}")
        except Exception as e:
            logging.error(f"Error storing law summary: {e}")

    async def get_law_summary(self, law_id):
        """
        Retrieves a law summary from the database.

        Args:
            law_id (str): ID of the law.

        Returns:
            str: The law summary, or None if not found.
        """
        try:
            async with aiosqlite.connect(self.db_path) as db:
                async with db.execute("""
                    SELECT summary FROM law_summaries WHERE law_id = ?
                """, (law_id,)) as cursor:
                    row = await cursor.fetchone()
                    if row:
                        return row[0]
                    else:
                        return None
        except Exception as e:
            logging.error(f"Error retrieving law summary: {e}")
            return None
