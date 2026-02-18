from  jose import jwt 
from  app.models.config import settings
from  datetime import datetime ,  timedelta  ,  timezone 

def create_access_token_jwt ( data : dict ,  expired_minutes :  int = None ) : 
    to_encode =  data.copy ( ) 
    expire = datetime.now(timezone.utc)   +  + timedelta(minutes=expired_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update ( {"exp": expire})
    encoded_jwt = jwt.encode( to_encode ,  settings.SECRET_KEY , algorithm=settings.ALGORITHM)
    return  encoded_jwt 

