import os 
from dotenv import load_dotenv
import redis 

load_dotenv( )

redis_url = os.getenv("REDISURL")

redis_client = redis.Redis.from_url(redis_url, decode_responses=True)

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