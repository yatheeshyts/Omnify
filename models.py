from pydantic import BaseModel
from datetime import datetime


class Classes(BaseModel):
    class_id:int
    name:str 
    start_time:datetime
    end_time:datetime
    instructor:str
    no_of_slots:int
    filled_slot:int

class Book(BaseModel):
    class_id:int
    client_name:str
    client_email:str

class Classes_info(BaseModel):
    class_id:int
    client_name:str
    class_name:str 
    start_time:datetime
    end_time:datetime
    instructor:str


class Booked_info(BaseModel):
    client_email:str
    class_info:list[Classes_info]

class Response(BaseModel):
    status:str
    message:str
