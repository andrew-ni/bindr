import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()



class Student(Base):
    __tablename__ = 'student'

    id = Column(Integer, primary_key=True)
    name = Column(String(250),nullable=False)
    description = Column(String(250),nullable=False)

    @property
    def serialize(self):
        return {
        'name': self.name,
        'id': self.id,
        'description': self.description
    }

class Event(Base):
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True)
    name = Column(String(250),nullable=False)
    loc_name = Column(String(250),nullable=False)
    loc_lat = Column(Float(10,6),nullable=False)
    loc_long = Column(Float(10,6),nullable=False)
    subject = Column(String(20),nullable=False)
    strt = Column(Date(),nullable=False)
    end = Column(Date(),nullable=False)
    desc = Column(String(250),nullable=False)
    



engine = create_engine('sqlite:///students.db')


Base.metadata.create_all(engine)