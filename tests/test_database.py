import database

def test_database_tables(tmp_path, monkeypatch):
    test_db = tmp_path / "test_security_logs.db"

    monkeypatch.setattr(database, "DATABASE", str(test_db))

    database.init_db()

    connection = database.get_connection()

    tables = connection.execute(
        "SELECT name FROM sqlite_master WHERE type ='table'"
    ).fetchall()

    connection.close()

    table_names = {row[0] for row in tables}

    assert "uploads" in table_names
    assert "events" in table_names
    assert "alerts" in table_names

def test_foreign_keys_enabled(tmp_path, monkeypatch):
    test_db  = tmp_path / "test_security_logs.db"

    monkeypatch.setattr(database, "DATABASE", str(test_db))

    connection = database.get_connection()

    result = connection.execute(
        "PRAGMA foreign_keys"
    ).fetchone()

    connection.close()

    assert result[0] == 1