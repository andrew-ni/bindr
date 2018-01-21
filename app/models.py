import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
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



engine = create_engine('sqlite:///students.db')


Base.metadata.create_all(engine)