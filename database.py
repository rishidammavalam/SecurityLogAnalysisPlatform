import sqlite3

DATABASE = "security_logs.db"

def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection

def init_db():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS uploads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            uploaded_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            upload_id INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            ip_address TEXT NOT NULL,
            username TEXT NOT NULL,
            event_type TEXT NOT NULL,
            FOREIGN KEY (upload_id) REFERENCES uploads(id)
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            upload_id INTEGER NOT NULL,
            alert_type TEXT NOT NULL,
            source_ip TEXT NOT NULL,
            failed_attempts INTEGER NOT NULL,
            severity TEXT NOT NULL,
            mitre_id TEXT NOT NULL,
            FOREIGN KEY (upload_id) REFERENCES uploads(id)
        )
    """)

    connection.commit()
    connection.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully")