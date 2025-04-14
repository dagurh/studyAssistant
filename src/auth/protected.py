from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from src.auth.utils import decode_access_token
from src.database import getUserByEmail

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if payload is None or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_email = payload["sub"]
    return await getUserByEmail(user_email)
