from  fastapi  import FastAPI 
from app.routers import  auth # there  are so many router 
from app.middleware.log_request import log_requests
from app.middleware.ip_rate_limit import rate_limit 
from  app.middleware.secure_headers import SecureHeaderMiddleware 
app = FastAPI ( title = "hassine  auth page")

app.middleware("http")(log_requests)
app.middleware("http")(rate_limit)
app.add_middleware(SecureHeaderMiddleware)
app.include_router ( auth.router ) 

# app.include_router ( auth.router ) 

## also 
###  uvicorn app.main:app --reload
 

@app.get("/test")
async def test_endpoint():
    return {"message": "ok"}