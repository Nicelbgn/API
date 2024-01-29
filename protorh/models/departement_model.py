from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Department(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True, index= True )                       
    Name = Column(String)                 

class AddUserToDepartment(BaseModel):

    id : str                       
    Name :str 

class GetUsersDepartRequest(BaseModel):

    id : str                       
    Name :str 

