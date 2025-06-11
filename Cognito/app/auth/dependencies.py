from fastapi import Depends, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer
from app.auth.cognito import CognitoClient

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://us-east-1cg0xai9sj.auth.us-east-1.amazoncognito.com/oauth2/authorize",
    tokenUrl="https://us-east-1cg0xai9sj.auth.us-east-1.amazoncognito.com/oauth2/token"
)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    cognito_client = CognitoClient()
    try:
        payload = cognito_client.verify_token(token)
        return payload
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")