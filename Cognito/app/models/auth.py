from pydantic import BaseModel

class SignUpRequest(BaseModel):
    username: str
    password: str
    email: str

class SignInRequest(BaseModel):
    username: str
    password: str

class ConfirmSignUpRequest(BaseModel):
    username: str
    confirmation_code: str
