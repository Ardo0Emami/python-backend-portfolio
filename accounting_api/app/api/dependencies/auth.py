from typing import Optional
from fastapi import Header, HTTPException, status
from accounting_api.app.core.config import settings


def get_api_key(x_api_key: str = Header(...)) -> Optional[str]:
    if x_api_key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )
