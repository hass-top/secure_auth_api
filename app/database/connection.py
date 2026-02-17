from sqlalchemy import create_engine ,  text
from sqlalchemy.orm import sessionmaker,declarative_base
from sqlalchemy.exc import SQLAlchemyError
from  app.models.config import settings

# a simple solution  for  env variable 
#import os
#from dotenv import load_dotenv
#load_dotenv( ) # to  load all  the envi variable 
#database_url= os.getenv("DATABASEURL")


if not settings.DATABASE_URL : 
    raise ValueError ( " database is  not  set")

engine = create_engine (                # connection  object 
    settings.DATABASE_URL , 
    pool_pre_ping = True  ,             # verify alive with ping 
    pool_size = 10 ,                    # max in  pool 
    max_overflow = 20                   # extra max 
)

made_session = sessionmaker (           # unit of working 
    autocommit = False ,                # change are conrole not automatic 
    autoflush = False ,                 #  to not write automatique in  db  
    bind = engine                       # sesion  create the  engine 
)

base =declarative_base ( )              # the  parent class 

def get_db ( ) : 
    db = made_session ( )
    try : 
        yield db 
    finally : 
        db.close( )

def test_connection():
    try:
        engine = create_engine(settings.DATABASE_URL)
        # Connect to DB
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1;"))
            print("DB Connection Successful:", result.scalar())
    except SQLAlchemyError as e:
        print("DB Connection Failed:", str(e))

if __name__ == "__main__":
    test_connection()