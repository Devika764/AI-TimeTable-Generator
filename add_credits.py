import sqlite3

try:
    conn = sqlite3.connect('instance/timetable.db')
    conn.execute("ALTER TABLE subject ADD COLUMN credits FLOAT DEFAULT 3.0")
    conn.commit()
    conn.close()
    print("Successfully added credits column")
except sqlite3.OperationalError as e:
    print("Column might already exist or error:", e)
