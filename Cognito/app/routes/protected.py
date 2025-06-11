from fastapi import APIRouter, Depends, HTTPException
from app.auth.dependencies import get_current_user

router = APIRouter()

@router.get("/me")
async def get_user(current_user: dict = Depends(get_current_user)):
    username = current_user.get("username")
    if not username:
        raise HTTPException(status_code=400, detail="Username not found in token")
    return {"message" :f"Welcome {username}"}