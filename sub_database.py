import logging
import aiosqlite

class DatabaseHandler:
    """Handles database operations for law summaries and corrections."""

    def __init__(self, db_path):
        """
        Initializes the DatabaseHandler with the database path.

        Args:
            db_path (str): Path to the SQLite database.
        """
        self.db_path = db_path

    async def build_database(self):
        """Creates the law summary and corrections database if it does not exist."""
        if not aiosqlite:
            logging.error("aiosqlite is not installed.")
            return

        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    """CREATE TABLE IF NOT EXISTS laws (
                                law_id INTEGER PRIMARY KEY,
                                summary TEXT
                            )"""
                )
                await db.execute(
                    """CREATE TABLE IF NOT EXISTS corrections (
                                situation_id TEXT PRIMARY KEY,
                                correction TEXT,
                                authorized_user TEXT,
                                timestamp DATETIME
                            )"""
                )
                await db.commit()
            logging.info("Law summary and corrections database created.")
        except aiosqlite.Error as e:
            logging.critical(f"Database creation error: {e}")
            raise

    async def check_database_health(self, health_check_duration, error_counter):
        """Checks the health of the law summary and corrections database."""
        try:
            with health_check_duration.time():
                async with aiosqlite.connect(self.db_path) as db:
                    await db.execute("SELECT 1")
                    await db.commit()
        except aiosqlite.Error as e:
            error_counter.inc()
            logging.error(f"Database health check failed: {e}")
            raise

    async def get_stored_correction(self, situation_id):
        """
        Retrieves a stored correction from the database.

        Args:
            situation_id (str): The ID of the situation.

        Returns:
            str: The stored correction as a JSON string, or None if not found.
        """
        try:
            async with aiosqlite.connect(self.db_path) as db:
                cursor = await db.execute(
                    "SELECT correction FROM corrections WHERE situation_id = ?",
                    (situation_id,),
                )
                result = await cursor.fetchone()
                if result:
                    return result[0]
                else:
                    return None
        except aiosqlite.Error as e:
            logging.error(f"Error retrieving correction: {e}")
            return None

    async def store_correction(self, situation_id, correction, authorized_user):
        """
        Stores a correction in the database.

        Args:
            situation_id (str): The ID of the situation.
            correction (str): The correction as a JSON string.
            authorized_user (str): The user who authorized the correction.
        """
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    "INSERT OR REPLACE INTO corrections (situation_id, correction, authorized_user, timestamp) VALUES (?, ?, ?, datetime('now'))",
                    (situation_id, correction, authorized_user),
                )
                await db.commit()
        except aiosqlite.Error as e:
            logging.error(f"Error storing correction: {e}")
