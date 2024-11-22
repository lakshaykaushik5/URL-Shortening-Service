from sqlalchemy import Column,Integer,String,DateTime
from sqlalchemy.orm import declarative_base
import datetime
from db_connection import db_config

Base = declarative_base()

class Data(Base):
    __tablename__ = "Data"
    
    id = Column(Integer,primary_key=True,index=True)
    url = Column(String(200),default=None)
    short_url = Column(String(100),default=None)
    created_at = Column(DateTime,default=datetime.datetime.utcnow)
    updated_at = Column(DateTime,default=datetime.datetime.utcnow,onupdate=datetime.datetime.utcnow)
    count = Column(Integer,default=0)
    
    def __repr__(self):
        return f"<DATA : {self.id} | {self.url} | {self.short_url} | {self.created_at} | {self.updated_at}>"
    
    
Base.metadata.create_all(bind=db_config.engine)