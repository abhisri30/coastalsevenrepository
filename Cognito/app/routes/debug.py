from fastapi import APIRouter
from app.auth.cognito import CognitoClient

router = APIRouter()

@router.get("/revoked-tokens")
async def get_revoked_tokens():
    cognito_client = CognitoClient()
    return {"revoked_token_hashes": list(cognito_client._revoked_tokens)}