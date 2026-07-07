import sqlite3

conn = sqlite3.connect('instance/timetable.db')
conn.execute('CREATE TABLE course (id INTEGER PRIMARY KEY, name VARCHAR(100) NOT NULL UNIQUE);')
conn.execute("INSERT INTO course (name) VALUES ('B.Tech');")
conn.commit()
conn.close()
print("Course table created and seeded with B.Tech")
