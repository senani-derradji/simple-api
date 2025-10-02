from db import base, engine
from sqlalchemy import Column, Integer, String

class User(base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key = True)
    name = Column(String, nullable=False)
    age = Column(Integer)
    grade = Column(String)

base.metadata.create_all(bind=engine)