from fastapi import status, HTTPException

import uuid

def validate_uuid(id: str) -> uuid.UUID:
    try:
        user_id = uuid.UUID(id, version=4)
        return user_id
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid id",
                    headers={
                        'Content-Type': 'application/json',
                        'WWW-Authenticate': 'Bearer'
                    })