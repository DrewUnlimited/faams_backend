from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from database import Base

class User(Base):
    __tablename__ = "users" 

    id = Column(Integer, primary_key=True, index=True) 
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(100), unique=True, index=True)
    password = Column(String(255))
    gender = Column(String(10))
    phone = Column(String(20))
    created_at = Column(TIMESTAMP, server_default=func.now())  
