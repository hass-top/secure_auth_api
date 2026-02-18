from  starlette.middleware.base import BaseHTTPMiddleware 
from  starlette.requests import Request 
from  starlette.responses import JSONResponse 
from  fastapi import status 
from app.models.config import settings
import redis 
redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)

class AuthMonitor( BaseHTTPMiddleware) : 
    async def dispatch(self, request : Request , call_next):
        
        if request.url.path != "/auth/login" : 
            return await call_next ( request )
        
        client_ip = request.client.host 
        max_attempts = settings.MAX_LOGIN_ATTEMPTS 
        block_time = settings.BLOCK_TIME_MINUTES 
        block_id = redis_client.get ( f"blocked:{client_ip}")
        if block_id :
            block_id_dt = datetime.fromisoformat(block_id) 
            if  datetime.utcnow() < block_id_dt : 
                return  JSONResponse (
                    {"detail" : "Too many failed login "},status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                )
            else : 
                redis_client.delete(f"brocked:{client_ip}")
    
        attempts = redis_client.get(f"attempts:{client_ip}")
        attempts = int(attempts) if attempts else 0
        request.state.client_ip = client_ip
        request.state.attempts = attempts 

        response = await call_next( request )
        return response