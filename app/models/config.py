from  pydantic_settings import  BaseSettings
import  os 
class  Settings ( BaseSettings ) : 
        SECRET_KEY : str 
        ALGORITHM : str 
        ACCESS_TOKEN_EXPIRE_MINUTES  : int 

        DATABASE_URL : str 

        REDIS_URL :  str 

        #AUTH monitoring 
        MAX_LOGIN_ATTEMPTS: int = 5
        BLOCK_TIME_MINUTES: int = 15



        class Config: 
            env_file = ".env"

settings = Settings( ) 