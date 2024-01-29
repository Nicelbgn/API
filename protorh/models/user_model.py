from sqlalchemy import Column, Integer, String, Date, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB
from pydantic import BaseModel
from datetime import datetime


Base = declarative_base()
class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index= True )                       
    email = Column(String)                 
    password = Column(String)     
    firstname = Column(String)             
    lastname = Column (String)    
    birthdaydate = Column (Date)            
    address = Column(String)             
    postalcode = Column (String)            
    age = Column (Integer)                      
    meta = Column (JSON)                    
    registrationdate = Column(Date)        
    token = Column(String)        
    role = Column(String)

class usersCreate(BaseModel):
                    
    email : str                
    password : str 
    firstname : str             
    lastname : str            
    birthdaydate : str          
    address : str           
    postalcode : str           
    age : int                             
    #RegistrationDate : int       
    #Token : str        
    role : str

class UploadProfilePicture(BaseModel):
     
    id : int                    
    Email : str                
    Password : str 
    Firstname : str             
    Lastname : str            
    BirthdayDate : int           
    Address : str           
    PostalCode : str           
    Age : int                             
    RegistrationDate : int       
    Token : str        
    Role : str
    file : str

class UpdatePassword(BaseModel):
                   
    email : str                
    password : str 
    new_password : str
    repeat_new_password :str

class Update(BaseModel):
    
    id: int
    email : str                
    password : str 
    firstname : str             
    lastname : str            
    birthdaydate : str          
    address : str           
    postalcode : str           
    age : int                             
    #RegistrationDate : int       
    #Token : str        
    role : str