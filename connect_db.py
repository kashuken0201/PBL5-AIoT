import sqlite3
import json
import datetime

DATABASE_DIR = 'PBL5/db.sqlite3'

con = sqlite3.connect(DATABASE_DIR)

cur = con.cursor()

cur.execute("SELECT * FROM USER_STUDENT")

print(cur.fetchall())
student_id = 0
t = datetime.datetime.now()

cur.execute("INSERT INTO facemask_log (date_time,student_id) values(?,?)", (t, student_id))

con.commit()