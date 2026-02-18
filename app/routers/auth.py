#---------------
from fastapi import APIRouter ,  Depends ,  HTTPException  ,  status  ,  Request  , Response , Cookie 
from  sqlalchemy.orm import Session  
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt 
from datetime import datetime , timedelta 
from typing import List
from sqlalchemy.exc import IntegrityError
#---------------
# from  my files
from  app.database.connection import get_db 
from app.auth.oauth2 import create_access_token_jwt 
from  app.auth.hashing import hash_password, verify_password 
from  app.models.user_models import User 
from  app.models.config import settings
from app.schemas.user_schema import RegisterUser
from  app.database.redis_conn import is_revoked  ,  revoke_token 
#---------------
#def router 
router = APIRouter(prefix="/auth" ,  tags = ["auth"])

# revoke token  in the redis memory with httponly !!!!! 
# the list that  are not  accepted 
revoked_tokens = set ( ) 


#------------
# POST /auth/register
@router.post("/register")# here  there  are  so many thin k to  do  
def register ( user : RegisterUser ,  db : Session = Depends ( get_db ))  : 

    if user.password != user.verificationpassword  : 
        raise HTTPException ( status_code = 400 ,  detail ="password do  not match")
    existing = db.query(User).filter( User.email == user.email ) .first( )  
    if existing : 
        raise HTTPException( status_code = 400 , detail  ="Email  alreadt existe")
    password_hash = hash_password(user.password)
    new_user_here =  User ( 
        name = user.name , 
        email = user.email , 
        password_hash = password_hash, 
        roles = "hamid" , 
        created_at=datetime.utcnow()

    )
    try : 
        db.add ( new_user_here )
        # before commit we need to  verify every think  in  the  orm  
        # wait 2 second 
        db.commit( )
        db.refresh ( new_user_here )
        return  { "message": "user creaed avec 100/% sure "}
    except IntegrityError : 
        db.rollback() 
        raise HTTPException ( status_code=400 , detail = "username or  email alrady existe ")
#------------

#------------
# POST /auth/login
@router.post("/login")
def login ( user : dict ,  db:Session = Depends ( get_db)) : 
    email = user.get( "email" ) 
    password = user.get ("password")

    db_user = db.query ( User ) .filter ( User.email == email).first ( ) 
    if  not db_user or not verify_password ( password , db_user.password_hash):
        raise HTTPException ( status_code = 401 ,  detail  = "invalid  credential or it can be not existe ")
    access_token = create_access_token_jwt ({"sub" : db_user.email, "roles" : db_user.roles.split(",")})
    expires_in  = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60 
    return { 
        "access_token" : access_token ,  
        "token_type" : "bearer" , 
        "expires_in" : expires_in 
    }
#------------


#------------
# POST /auth/refresh
@router.post("/refresh")
def refresh (request : Request , db: Session = Depends ( get_db ) ,  refresh_token  : str = Cookie(None)) : 
    if not refresh_token or   is_revoked(refresh_token) : 
        raise HTTPException ( status_code = 401 ,  detail="Invalid or expired ")
    try : 
        payload = jwt.decode ( refresh_token ,  settings.SECRET_KEY ,  algorithms=[settings.ALGORITHM])
        email = payload .get ( "sub") 
        roles = payload.get( "roles",[])
        # i  need  to add more  security here  as i think  
    except : 
        raise HTTPException ( status_code = 401 , detail ="invalid refreh_token" )
    access_token  =  create_access_token_jwt ( {"sub" : email ,  "roles" : roles })
    revoke_token(refresh_token, expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES*60)

    return  { 
        "access_token" : access_token , 
        "token_type" : "bearer" , 
        "expires_in" : settings.ACCESS_TOKEN_EXPIRE_MINUTES *60 

    }
#------------



#------------
# POST /auth/logout 
@router.post("/logout")
def logout( token: dict ) : 
    the_last_token_alive = token.get ( "access_token") 
    if not the_last_token_alive:
        raise HTTPException(status_code=400, detail="No token provided")

    try:
        payload = jwt.decode(the_last_token_alive, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        expires_in = payload.get("exp", 0) - int(datetime.utcnow().timestamp())
        if expires_in <= 0:
            expires_in = 1  
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    if is_revoked(the_last_token_alive):
        raise HTTPException(status_code=401, detail="Token already revoked")

    revoke_token(the_last_token_alive, expires_in=expires_in)
    return  { "message" : "logged from the  road "}
#------------


