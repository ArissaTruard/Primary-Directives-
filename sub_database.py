import logging
import aiosqlite
import httpx  # Import httpx for downloading full laws (simulated)

class DatabaseHandler:
    def __init__(self, db_path):
        self.db_path = db_path
        asyncio.run(self.build_database())

    async def build_database(self):
        """Builds the law summary database if it does not exist."""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    """
                    CREATE TABLE IF NOT EXISTS laws (
                        law_id TEXT PRIMARY KEY,
                        summary TEXT
                    )
                    """
                )
                await db.execute(
                    """
                    CREATE TABLE IF NOT EXISTS corrections (
                        situation_id TEXT PRIMARY KEY,
                        correction TEXT,
                        authorized_user TEXT
                    )
                    """
                )
                await db.commit()
            logging.info("Law summary database built successfully.")
        except aiosqlite.Error as e:
            logging.error(f"Error building law summary database: {e}")

    async def check_database_health(self, duration_histogram, error_counter):
        """Checks the health of the database."""
        try:
            start_time = time.time()
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("SELECT 1")
            duration_histogram.observe(time.time() - start_time)
            logging.info("Database health check successful.")
        except aiosqlite.Error as e:
            error_counter.inc()
            logging.error(f"Database health check failed: {e}")
            raise

    async def store_correction(self, situation_id, correction, authorized_user):
        """Stores a correction in the database."""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    """
                    INSERT OR REPLACE INTO corrections (situation_id, correction, authorized_user)
                    VALUES (?, ?, ?)
                    """,
                    (situation_id, correction, authorized_user),
                )
                await db.commit()
            logging.info(f"Correction stored for situation: {situation_id}")
        except aiosqlite.Error as e:
            logging.error(f"Error storing correction: {e}")

    async def get_stored_correction(self, situation_id):
        """Retrieves a stored correction from the database."""
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

    async def get_law_summary(self, law_id):
        """Retrieves a law summary from the database."""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                cursor = await db.execute("SELECT summary FROM laws WHERE law_id = ?", (law_id,))
                result = await cursor.fetchone()
                if result:
                    return result[0]
                else:
                    return None
        except aiosqlite.Error as e:
            logging.error(f"Error retrieving law summary: {e}")
            return None

    async def download_full_law(self, law_id):
        """Simulates downloading the full law text."""
        try:
            # Simulate downloading the full law text
            law_summary = await self.get_law_summary(law_id)
            if law_summary:
                # In a real system, you would fetch the full law from an external source.
                # Here, we just return a simulated full law text.
                return f"Full law text for law ID {law_id}: {law_summary} (Simulated download)"
            else:
                return None
        except Exception as e:
            logging.error(f"Error simulating full law download: {e}")
            return None
