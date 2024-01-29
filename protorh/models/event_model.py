from pydantic import BaseModel
from main import Base
from sqlalchemy import Column, Integer, String, Date

class Event(Base):
    _tablename_ = "Event"

    id = Column(Integer, primary_key=True, index= True )                       
    Name = Column(String)                 
    Date = Column(Date)     
    Description = Column(String)             
    UserID = Column(Integer)              
    DepartmentID = Column(Integer)            
    
class CreateEvent(BaseModel):

    id : str
    Name :str
    Date : int
    Description : str
    UserID : int
    DepartmentID : int
