from  fastapi  import FastAPI 

#---------

from app.routers import  auth # there  are so many router 
from app.middleware.log_request import log_requests
from app.middleware.ip_rate_limit import rate_limit 
from  app.middleware.auth_monitor import AuthMonitor 
from  app.middleware.jwt_verification import JWTVerificationMiddleware 
from  app.middleware.secure_headers import SecureHeaderMiddleware 

#---------

app = FastAPI ( title = "hassine  auth page")

#----------

from  fastapi.middleware.cors  import CORSMiddleware 
app.add_middleware ( 
    CORSMiddleware , 
    # allow_origins =[]  this is only for front  end  
    allow_credentials = True , 
    allow_methods = ["GET" , "POST" , "PATCH" , "DELETE"] , 
    allow_headers = ["*"] ,
)

#----------
app.add_middleware(AuthMonitor)
app.middleware("http")(log_requests)
app.middleware("http")(rate_limit)
app.add_middleware(SecureHeaderMiddleware)
app.add_middleware(JWTVerificationMiddleware)

#---------

app.include_router ( auth.router ) 

@app.get("/test") 
async def test_endpoint():
    return {"message": "ok"} 
## also 
###  uvicorn app.main:app --reload
