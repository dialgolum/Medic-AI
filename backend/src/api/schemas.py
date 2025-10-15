from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    name: str
    age: int
    gender: str

class UserInDB(BaseModel):
    username: str
    name: str
    age: int
    gender: str

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginRequest(BaseModel):
    username: str
    password: str