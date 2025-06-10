from datetime import datetime
import sqlite3

conn = sqlite3.connect("BOOKING.db")
conn.row_factory = sqlite3.Row
cur = conn.cursor()



cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='CLASSES'")
output = cur.fetchall()
if not output:
    cur.execute("""CREATE TABLE CLASSES(class_id integer primary key AUTOINCREMENT, 
                name string, 
                start_time string, 
                end_time string, 
                instructor string, 
                no_of_slots integer, 
                filled_slots integer)""")
    
cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='BOOKINGS'")
output = cur.fetchall()
if not output:
    cur.execute("""CREATE TABLE BOOKINGS(class_id integer, 
                client_name string, 
                client_email string)""")
    
cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='LOGS'")
output = cur.fetchall()
if not output:
    cur.execute("""CREATE TABLE LOGS(log_id integer, 
                log_entry string, 
                time_stamp string)""")





data = [
    ("Evening Zumba",datetime(2025, 6, 10, 16, 0).strftime("%Y-%m-%d %H:%M:%S"), datetime(2025, 6, 10, 17, 0).strftime("%Y-%m-%d %H:%M:%S"), "Ramesh", 5, 0),
    ("Morning Zumba",datetime(2025, 6, 10, 8, 0).strftime("%Y-%m-%d %H:%M:%S"), datetime(2025, 6, 10, 9, 0).strftime("%Y-%m-%d %H:%M:%S"), "Dinesh", 5, 0),
    ("Morning",datetime(2025, 6, 10, 8, 30).strftime("%Y-%m-%d %H:%M:%S"), datetime(2025, 6, 10, 9, 30).strftime("%Y-%m-%d %H:%M:%S"), "Suresh", 5, 0),
]
cur.executemany("INSERT INTO CLASSES (name, start_time, end_time, instructor, no_of_slots, filled_slots) VALUES(?, ?, ?, ?, ?, ?)", data)
# cur.execute("UPDATE CLASSES SET FILLED_SLOTS=2 WHERE CLASS_ID=1)")
# cur.execute("SELECT * FROM BOOKINGS B, CLASSES C WHERE C.CLASS_ID=B.CLASS_ID and b.client_email='string1'")




    




conn.commit()
conn.close()

