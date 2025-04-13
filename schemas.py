from pydantic import BaseModel, EmailStr

# Schema for the user during sign-up
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    gender: str
    phone: str
    password: str
    password_confirmation: str

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True
