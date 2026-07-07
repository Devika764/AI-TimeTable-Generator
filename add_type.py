import sqlite3

try:
    conn = sqlite3.connect('instance/timetable.db')
    conn.execute("ALTER TABLE subject ADD COLUMN subject_type VARCHAR(20) DEFAULT 'Theory'")
    conn.commit()
    conn.close()
    print("Successfully added subject_type column")
except sqlite3.OperationalError as e:
    print("Column might already exist or error:", e)
