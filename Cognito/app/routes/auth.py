from fastapi import APIRouter, Depends, HTTPException, Header
from app.auth.cognito import CognitoClient
from app.models.auth import SignUpRequest, SignInRequest, ConfirmSignUpRequest
router = APIRouter()

@router.post("/signup")
async def signup(signup_data: SignUpRequest):
    cognito_client = CognitoClient()
    response = cognito_client.sign_up(
        username=signup_data.username,
        password=signup_data.password,
        email=signup_data.email
    )
    return {"message": "User signed up successfully", "response": response}

@router.post("/confirm-signup")
async def confirm_signup(confirm_data: ConfirmSignUpRequest):
    cognito_client = CognitoClient()
    response = cognito_client.confirm_sign_up(
        username=confirm_data.username,
        confirmation_code=confirm_data.confirmation_code
    )
    return {"message": "User confirmed successfully", "response": response}

@router.post("/signin")
async def signin(signin_data: SignInRequest):
    cognito_client = CognitoClient()
    response = cognito_client.sign_in(
        username=signin_data.username,
        password=signin_data.password
    )
    return {"message": "User signed in successfully", "tokens": response}

@router.post("/signout")
async def signout(authorization: str = Header(...)):
    cognito_client = CognitoClient()
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=400, detail="Invalid Authorization header format")
    access_token = authorization.split(" ")[1]
    response = cognito_client.sign_out(access_token=access_token)
    return {"message": "User signed out successfully", "response": response}