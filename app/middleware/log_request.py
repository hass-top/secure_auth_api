from  fastapi  import Request 
import time 

async def log_requests ( request  ,  call_next ) : 
    start_time = time.time ( ) 
    response = await call_next( request ) 
    process_time = time.time () - start_time 
    print( f"{request.method} {request.url.path} completed in {process_time:.4f}s")
    return  response 

