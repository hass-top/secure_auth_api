from  fastapi.middleware.cors  import CORSMiddleware 
from  app.main import  app  

app.add_middleware ( 
    CORSMiddleware , 
    # allow_origins =[]  this is only for front  end  
    allow_credentials = True , 
    allow_methods = ["GET" , "POST" , "PATCH" , "DELETE"] , 
    allow_headers = ["*"] ,
 )