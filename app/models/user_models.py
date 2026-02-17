from app.database.connection import base ,  engine 
from  sqlalchemy import Column  , Integer , String , DateTime
from datetime import datetime
class User ( base ):
    __tablename__ = "users"
    id =Column ( Integer , primary_key = True ,  index= True )
    name = Column ( String ,  unique= True ,  index = True )
    password_hash  =  Column  ( String )
    roles =  Column  ( String )
    email = Column (String ,  unique=True ,index = True )
    created_at = Column(DateTime, default=datetime.utcnow)
# made other tables here 

if  __name__ == "__main__" : 
    base.metadata.create_all( bind=engine )
    print ( "Tables created successfully ")
