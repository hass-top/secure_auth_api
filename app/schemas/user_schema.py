from pydantic import BaseModel, EmailStr , constr

class RegisterUser(BaseModel):
    name: str
    email: EmailStr
    password: constr(min_length=6, max_length=72)
    verificationpassword: constr(min_length=6, max_length=72)