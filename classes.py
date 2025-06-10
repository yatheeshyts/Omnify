from sqlite3 import Connection
from datetime import datetime
from models import Classes, Book

def get_classes(conn:Connection)-> list[Classes]:
    """returns all classes registered in the system."""
    cur = conn.cursor()
    cur.execute("SELECT * FROM CLASSES")
    output = cur.fetchall()
    result = []
    for i in output:
        cls=dict(zip(i.keys(), i))
        result.append(Classes(class_id=cls["class_id"], 
                              name=cls["name"],
                              start_time=datetime.strptime(cls["start_time"], "%Y-%m-%d %H:%M:%S"),
                              end_time=datetime.strptime(cls["end_time"], "%Y-%m-%d %H:%M:%S"),
                              instructor=cls["instructor"],
                              no_of_slots=cls["no_of_slots"],
                              filled_slot=cls["filled_slots"]))
    return result

def is_exist(conn:Connection, class_id:int)->bool:
    """Checks if class is presents or not"""
    cur = conn.cursor()
    cur.execute("SELECT * FROM CLASSES WHERE CLASS_ID={}".format(class_id))
    if cur.fetchall():
        return True
    else:
        return False

def is_conflict(conn:Connection, book:Book):
    cur = conn.cursor()
    cur.execute("SELECT * FROM CLASSES WHERE CLASS_ID='{}' ".format(book.class_id))
    output = cur.fetchall()
    new_class = dict(zip(output[0].keys(), output[0]))
    new_time = [datetime.strptime(new_class["start_time"], "%Y-%m-%d %H:%M:%S"),
                datetime.strptime(new_class["end_time"], "%Y-%m-%d %H:%M:%S")]
    cur.execute("SELECT * FROM BOOKINGS B, CLASSES C WHERE C.CLASS_ID=B.CLASS_ID and b.client_email='{}' ".format(book.client_email))
    output = cur.fetchall()
    old_class = []
    for i in output:
        old_class = dict(zip(i.keys(), i))
        old_time = [datetime.strptime(old_class["start_time"], "%Y-%m-%d %H:%M:%S"),
                    datetime.strptime(old_class["end_time"], "%Y-%m-%d %H:%M:%S")]
        if not(new_time[0] >= old_time[1] or old_time[0] >= new_time[1]):
            return True
    return False
