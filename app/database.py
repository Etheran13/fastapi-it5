"""SQLite connection and table setup."""

import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

DATABASE_FILE = Path(__file__).resolve().parent.parent / "bookings.db"


@contextmanager
def database_connection() -> Iterator[sqlite3.Connection]:
    """Open a database connection and always close it after the operation."""

    connection = sqlite3.connect(DATABASE_FILE)
    connection.row_factory = sqlite3.Row
    # Enforce foreign key constraints in SQLite
    connection.execute("PRAGMA foreign_keys = ON")
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def initialize_database() -> None:
    """Create the rooms and bookings tables the first time the app runs."""

    with database_connection() as connection:
        # Table 1: Rooms (Primary Table)
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS rooms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                capacity INTEGER NOT NULL CHECK (capacity >= 1)
            )
            """
        )
        
        # Table 2: Bookings (Related Table with Foreign Key)
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS bookings (
                booking_number INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                amount_of_guests INTEGER NOT NULL CHECK (amount_of_guests >= 1),
                payment_status TEXT NOT NULL,
                room_id INTEGER NOT NULL,
                FOREIGN KEY(room_id) REFERENCES rooms(id)
            )
            """
        )