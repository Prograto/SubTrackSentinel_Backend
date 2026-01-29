from pydantic import BaseModel, EmailStr

class RegisterUser(BaseModel):
    username: str
    email: EmailStr
    password: str
    phone: str
    role: str = "user" 
    
class LoginUser(BaseModel):
    email: EmailStr
    password: str
