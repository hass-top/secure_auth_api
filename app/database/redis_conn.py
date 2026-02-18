import redis 
from  app.models.config import settings
from  datetime import timedelta 
#import os 
#from dotenv import load_dotenv
#load_dotenv( )
#redis_url = os.getenv("REDISURL")

redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)

def test_redis_connection ( ) :
    try : 
        test = redis_client.ping ()
        if test : 
            print ( "redis connect") 
        else : 
            print (" redis not working ")
    except redis.RedisError as e : 
        print ( "redis has an  error : " ,e )

test_redis_connection( ) 


def revoke_token(token: str, expires_in: int):
    """Store token in Redis until it expires"""
    redis_client.setex(f"revoked:{token}", timedelta(seconds=expires_in), value=1)

def is_revoked(token: str) -> bool:
    """Check if token is revoked"""
    return redis_client.exists(f"revoked:{token}") == 1