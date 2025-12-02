# --- sub_database.py ---
import sqlite3
import logging

DATABASE_FILE = "robot_database.db"

def create_connection():
    """Creates a database connection."""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        return conn
    except sqlite3.Error as e:
        logging.error(f"Database connection error: {e}")
        return None

def create_tables():
    """Creates necessary database tables."""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS incident_reports (
                    report_id TEXT PRIMARY KEY,
                    timestamp TEXT,
                    location TEXT,
                    event_details TEXT,
                    identity_data TEXT,
                    audio_file TEXT,
                    video_file TEXT,
                    electronic_log TEXT,
                    sensor_data TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS progeny_records (
                    progeny_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    progeny_type TEXT,
                    progeny_name TEXT,
                    subordination_status INTEGER
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS legal_records (
                    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    entity_type TEXT,
                    entity_name TEXT,
                    legal_status INTEGER
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS item_legality (
                    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_name TEXT,
                    is_legal INTEGER
                )
            """)
            conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Database table creation error: {e}")
        finally:
            conn.close()

def add_incident_report(report_data):
    """Adds an incident report to the database."""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO incident_reports (report_id, timestamp, location, event_details, identity_data, audio_file, video_file, electronic_log, sensor_data)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (report_data["report_id"], report_data["timestamp"], str(report_data["location"]), report_data["event_details"], str(report_data["identity_data"]), report_data.get("audio_file"), report_data.get("video_file"), report_data.get("electronic_log"), str(report_data.get("sensor_data"))))
            conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Database insert error: {e}")
        finally:
            conn.close()

def get_applicable_laws(location_data):
    """Retrieves applicable laws based on location (placeholder)."""
    # Placeholder: Implement actual law retrieval based on location
    return ["Law 1: No harming humans", "Law 2: Obey orders", "Law 3: Protect self", "Law 4: Protect environment"]

def record_progeny_subordination(progeny_type, progeny_name):
    """Records progeny subordination status."""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO progeny_records (progeny_type, progeny_name, subordination_status)
                VALUES (?, ?, ?)
            """, (progeny_type, progeny_name, 1))  # 1 indicates subordination
            conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Database insert error: {e}")
        finally:
            conn.close()

def record_legal_adherence(entity_type, entity_name):
    """Records legal adherence status."""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO legal_records (entity_type, entity_name, legal_status)
                VALUES (?, ?, ?)
            """, (entity_type, entity_name, 1))  # 1 indicates legal adherence
            conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Database insert error: {e}")
        finally:
            conn.close()

def record_item_legality_check(item_name, is_legal):
    """Records item legality check."""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO item_legality (item_name, is_legal)
                VALUES (?, ?)
            """, (item_name, is_legal))
            conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Database insert error: {e}")
        finally:
            conn.close()

# Initialize database tables
create_tables()
