import sqlite3

try:
    conn = sqlite3.connect('instance/timetable.db')
    conn.execute("ALTER TABLE subject ADD COLUMN regulation VARCHAR(50) DEFAULT 'R20'")
    conn.commit()
    conn.close()
    print("Successfully added regulation column")
except sqlite3.OperationalError as e:
    print("Column might already exist or error:", e)
