import time

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app import models
from config import settings

bearer_scheme = HTTPBearer()


def get_user(db, user_id: int) -> models.User:
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="jwtの設定が正しくありません",
        )

    return user


def get_user_and_decode_access_token(
    authorization: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    db: Session = Depends(settings.get_db),
):
    if authorization is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="jwtが正しく設定されていません",
        )

    user_id = user_id_from_access_token(authorization.credentials)
    return get_user(db, user_id)


def create_access_token(user: models.User) -> str:
    return _create_jwt_token(
        user,
        int(time.time()) + settings.JWT_ACCESS_TOKEN_EXPIRES_SECONDS,
        "access_token",
    )


def create_refresh_token(user: models.User) -> str:
    return _create_jwt_token(
        user,
        int(time.time()) + settings.JWT_REFRESH_TOKEN_EXPIRES_SECONDS,
        "refresh_token",
    )


def user_id_from_access_token(
    access_token: str = Depends(HTTPBearer()),
) -> int:
    """
    access_tokenの検証を行いuser_idを取得する
    """
    payload = _decode_jwt_token(access_token, "access_token")

    return payload["user_id"]


def user_id_from_refresh_token(refresh_token: str) -> int:
    """
    refresh_tokenの検証を行いuser_idを取得する
    """
    payload = _decode_jwt_token(refresh_token, "refresh_token")

    return payload["user_id"]


def _create_jwt_token(user: models.User, exp: int, typ: str) -> str:
    payload = {
        "user_id": user.id,
        "exp": exp,
        "typ": typ,
    }

    encoded_jwt = jwt.encode(
        payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )

    return encoded_jwt


def _decode_jwt_token(access_token: str, typ: str) -> dict:
    try:
        payload = jwt.decode(
            access_token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="jwtが正しく設定されていません",
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="jwtが正しく設定されていません",
        )

    if payload["typ"] != typ:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="jwtが正しく設定されていません",
        )

    return payload
