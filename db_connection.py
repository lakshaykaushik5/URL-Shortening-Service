from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from  contextlib import contextmanager
import os

from dotenv import load_dotenv
load_dotenv()



class db_connection:
    def __init__(self):
        self.Database_url = os.getenv('DATABASE_URL')
            
    
        self.engine = create_engine(
            self.Database_url,
            pool_size=5,
            max_overflow=15,
            pool_timeout=30,
            pool_recycle=1800,
            echo=True
        )
        
        self.sessionLocal = sessionmaker(
            bind = self.engine,
            autoflush=False,
            autocommit=False
        )
        
    @contextmanager
    def get_db_session(self):
        session = self.sessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            raise e
        finally:
            session.close()


db_config = db_connection()
        

