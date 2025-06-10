from models import Book, Classes, Booked_info, Classes_info
from datetime import datetime
from sqlite3 import Connection
import re

def get_booking(conn:Connection, email:str)->Booked_info:
    """returns all the bookings done by individual e-mail."""
    cur = conn.cursor()
    cur.execute("SELECT * FROM BOOKINGS B, CLASSES C WHERE C.CLASS_ID=B.CLASS_ID and b.client_email= '{}'".format(email))
    output = cur.fetchall()
    result = []
    for i in output:
        cls=dict(zip(i.keys(), i))
        result.append(
            Classes_info(
                class_id=cls["class_id"],
                client_name=cls["client_name"],
                class_name=cls["name"],
                start_time=datetime.strptime(cls["start_time"], "%Y-%m-%d %H:%M:%S"),
                end_time=datetime.strptime(cls["end_time"], "%Y-%m-%d %H:%M:%S"),
                instructor=cls["instructor"],
            )
        )
    return Booked_info(
        client_email=email,
        class_info=result
    )

def create_booking(conn:Connection, book:Book)->bool:
    """registers booking to server."""
    cur = conn.cursor()
    cur.execute("SELECT * FROM CLASSES WHERE CLASS_ID={}".format(book.class_id))
    output = cur.fetchone()
    cls=dict(zip(output.keys(), output))
    if cls["filled_slots"] < cls["no_of_slots"]:
        cur.execute("INSERT INTO BOOKINGS (class_id, client_name, client_email) VALUES(?, ?, ?)",(book.class_id, book.client_name, book.client_email))
        cur.execute("UPDATE CLASSES SET FILLED_SLOTS=? WHERE CLASS_ID=?",(cls["filled_slots"]+1, book.class_id))
        conn.commit()
        return True
    else:
        return False


def is_exist(conn:Connection, book:Book)->bool:
    """Checks if booking is presents or not"""
    cur = conn.cursor()
    cur.execute("SELECT * FROM BOOKINGS WHERE CLASS_ID=? and CLIENT_EMAIL = ?", (book.class_id,book.client_email))
    if cur.fetchall():
        return True
    else:
        return False
    
def is_email(email:str)->bool:
    pattern=r"^[a-zA-Z]+@[a-zA-Z]+\.[a-zA-Z]+"
    if re.search(pattern,email):
        return True
    else:
        return False
    



    