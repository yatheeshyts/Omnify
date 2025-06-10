from fastapi import FastAPI
import uvicorn, classes as c, booking as b
from models import Classes, Book, Response, Booked_info
import config
import sqlite3

# DB Connection
conn = sqlite3.connect(config.DB_URL, check_same_thread=False)
conn.row_factory = sqlite3.Row

app = FastAPI()

@app.get("/classes")
def get_classes()-> list[Classes]:
    """This URL returns all classes and its availabilities."""
    return c.get_classes(conn)

@app.post("/book")
def book(book:Book)->Response:
    """This URL is used to reserve slot for individual by e-mail."""
    if not b.is_email(book.client_email):
        return Response(status=config.FAIL,message=config.MSG_EMAIL.format(book.client_email))
    if b.is_exist(conn, book):
        return Response(status=config.FAIL,message=config.MSG_BOOKING_EXIST.format(book.class_id, book.client_email))
    elif not c.is_exist(conn,book.class_id):
         return Response(status=config.FAIL,message=config.MSG_CLASS_NOT_FOUND.format(book.class_id))
    elif c.is_conflict(conn,book):
        return Response(status=config.FAIL,message=config.MSG_CONFLICT(book.client_email, book.class_id))
    elif b.create_booking(conn,book):
        return Response(status=config.PASS,message=config.MSG_BOOKING_SUCCESS.format(book.client_email, book.class_id))
    else:
        return Response(status=config.FAIL,message=config.MSG_SLOT_FULL.format(book.class_id))

@app.get("/booking/{email}")
def booking(email)->Booked_info:
    """This URL will return all the bookings for individual by e-mail."""
    return b.get_booking(conn, email)