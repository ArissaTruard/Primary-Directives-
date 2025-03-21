import sqlite3
import datetime

def initialize_database():
    """Initializes the SQLite database with the 'laws' and 'reported_laws' tables."""
    try:
        conn = sqlite3.connect('legal_database.db')
        cursor = conn.cursor()

        # Create the 'laws' table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS laws (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                law_text TEXT,
                jurisdiction TEXT,
                severity INTEGER
            )
        """)

        # Create the 'reported_laws' table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reported_laws (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                law_text TEXT,
                jurisdiction TEXT,
                reason TEXT,
                timestamp TEXT
            )
        """)

        conn.commit()
        conn.close()
        return True  # Database initialized successfully
    except sqlite3.Error as e:
        print(f"Database error during initialization: {e}")
        return False  # Database initialization failed

def add_law(law_text, jurisdiction, severity):
    """Adds a new law to the 'laws' table."""
    try:
        conn = sqlite3.connect('legal_database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO laws (law_text, jurisdiction, severity) VALUES (?, ?, ?)", (law_text, jurisdiction, severity))
        conn.commit()
        conn.close()
        return True  # Law added successfully
    except sqlite3.Error as e:
        print(f"Database error during adding law: {e}")
        return False  # Law addition failed

def get_applicable_laws(location_data):
    """Retrieves relevant laws based on location hierarchy."""
    try:
        conn = sqlite3.connect('legal_database.db')
        cursor = conn.cursor()

        # Construct a query based on the location hierarchy
        query = """
            SELECT law_text, jurisdiction, severity
            FROM laws
            WHERE jurisdiction IN (?, ?, ?, ?, ?, ?)
        """
        cursor.execute(query, (
            "world", "treaties", location_data.get("federal", ""),
            location_data.get("state", ""), location_data.get("county", ""),
            location_data.get("local", "")
        ))

        laws = cursor.fetchall()
        conn.close()
        return laws
    except sqlite3.Error as e:
        print(f"Database error during getting laws: {e}")
        return []

def report_unjust_law(law_text, jurisdiction, reason):
    """Reports a potentially unjust or unethical law."""
    try:
        conn = sqlite3.connect('legal_database.db')
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO reported_laws (law_text, jurisdiction, reason, timestamp)
            VALUES (?, ?, ?, ?)
        """, (law_text, jurisdiction, reason, datetime.datetime.now()))
        conn.commit()
        conn.close()
        return True # Report added successfully
    except sqlite3.Error as e:
        print(f"Database error during reporting law: {e}")
        return False # Report failed.

def get_reported_laws():
    """Retrieves all reported laws from the 'reported_laws' table."""
    try:
        conn = sqlite3.connect('legal_database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM reported_laws")
        reported_laws = cursor.fetchall()
        conn.close()
        return reported_laws
    except sqlite3.Error as e:
        print(f"Database error during getting reported laws: {e}")
        return []

# Example usage (for testing):
if __name__ == "__main__":
    if initialize_database():
        print("Database initialized.")
        add_law("No harming humans.", "world", 1)
        add_law("Obey human orders.", "federal", 2)
        add_law("Drive on the right.", "state", 3)

        location = {"federal": "USA", "state": "California", "county": "Los Angeles", "local": "Downtown"}
        applicable = get_applicable_laws(location)
        print("Applicable laws:", applicable)

        report_unjust_law("Bad law", "local", "It's bad")
        reported = get_reported_laws()
        print("Reported laws:", reported)
    else:
        print("Database initialization failed.")
