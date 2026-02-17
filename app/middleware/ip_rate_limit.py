from starlette.responses import JSONResponse
from  fastapi import Request ,  HTTPException  
from datetime import datetime , timedelta 

ip_request_count = {}
async def rate_limit ( request : Request ,  call_next ) : 
    ip  = request.client.host
    now = datetime.utcnow () 

    ip_request_count [ip] = [t for t in  ip_request_count.get(ip ,  []) if now -t < timedelta ( minutes = 1 )]


    # Check if limit exceeded
    if len(ip_request_count[ip]) >= 10:
        # Return proper 429 response instead of raising
        return JSONResponse(status_code=429, content={"detail": "Too many requests"})

    ip_request_count [ip].append ( now ) 
    response = await call_next ( request ) 
    return  response 