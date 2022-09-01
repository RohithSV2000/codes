from importlib.metadata import metadata
from msilib import schema
from optparse import Values
from sqlalchemy import create_engine
from sqlalchemy.schema import Index
import socketserver


import cx_Oracle
from fastapi import FastAPI
from pydantic import BaseModel
 
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey




host='127.0.0.1'
port=1521
sid='xe'
user='system'
password='oracle'

cstr = "oracle://system:oracle@localhost:1521/xe"
engine =  create_engine(
    cstr
)



metadata_obj = MetaData()
user = Table('usermaster', metadata_obj,
Column('id', Integer, primary_key=True),
Column('name', String(30)),
Column('fullname', String(30)),
 )


class User(BaseModel):
    id:int
    name:str
    fullname:str

metadata_obj.create_all(engine)

conn=engine.connect()

users=FastAPI()
@users.get("/")
def root():
    return conn.execute(user.select()).fetchall()

@users.get("/{id}")
def root(id:int):
    return conn.execute(user.select().where (user.c.id==id)).fetchall()
    

@users.post("/")
def write_data(userinfo:User):
  return[conn.execute(user.insert().values
                         (id=userinfo.id,
                          name =userinfo.name,
                         fullname=userinfo.fullname
                        
                        ))]
@users.put("/{id}")
def update_data( id:int ,userinfo:User):
  conn.execute(user.update().values
                         (id=userinfo.id,
                          name =userinfo.name,
                         fullname=userinfo.fullname
                        
                        ).where(user.c.id==id))
  return conn.execute(user.select().where (user.c.id==id)).fetchall()