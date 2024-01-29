from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB
from pydantic import BaseModel, Json



Base = declarative_base()

class RequestRH(Base):
    __tablename__ = "RequestRH"

    id = Column(Integer, primary_key=True, index= True )                                     
    UserId = Column(Integer)     
    Content = Column(String)             
    RegistrationDate = Column (Date)              
    Visibility = Column()            
    Close = Column(Boolean)             
    LastAction= Column(Date)                                  
    ContentHistory = Column(JSONB)                    
    

class CreateRequestRH(BaseModel):

    #id : str  
    user_id : int     
    content : str            

class RemoveRequestRH(BaseModel):

    id : str  
    UserId : int     
    Content : str            
    RegistrationDate : int              
    Visibility : bool            
    Close : bool            
    LastAction : int                                  
    ContentHistory : Json