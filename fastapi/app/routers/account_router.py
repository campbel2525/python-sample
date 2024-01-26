from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models
from app.auth import authentication
from app.schemas.requests import account_request
from app.schemas.responses import account_response
from config import settings, swagger_config

router = APIRouter()


@router.post(
    "/v1/accounts/sign-up",
    response_model=account_response.JwtResponse,
    summary=str(swagger_config.get_schemas()["accounts_sign_up"]["summary"]),
    description=str(swagger_config.get_schemas()["accounts_sign_up"]["description"]),
    tags=list(swagger_config.get_schemas()["accounts_sign_up"]["tags"]),
)
async def sign_up(
    request: account_request.SignUpRequest,
    db: Session = Depends(settings.get_db),
) -> account_response.JwtResponse:
    """
    新規登録
    """
    # すでに登録済みでないか
    is_exist = models.User.exist_user(db, request.email)
    if is_exist is True:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="すでに登録済みのメールアドレスです。"
        )

    # ユーザーを登録
    user = models.User()
    user.name = request.name
    user.email = request.email
    user.password = models.User.password_to_hash(request.password)
    db.add(user)
    db.commit()
    db.refresh(user)

    # トークンを返す
    access_token = authentication.create_access_token(user)
    refresh_token = authentication.create_refresh_token(user)
    return account_response.JwtResponse(
        access_token=access_token, refresh_token=refresh_token
    )


@router.post(
    "/v1/accounts/sign-in",
    response_model=account_response.JwtResponse,
    summary=str(swagger_config.get_schemas()["accounts_sign_in"]["summary"]),
    description=str(swagger_config.get_schemas()["accounts_sign_in"]["description"]),
    tags=list(swagger_config.get_schemas()["accounts_sign_in"]["tags"]),
)
async def sign_in(
    request: account_request.SignInRequest,
    db: Session = Depends(settings.get_db),
) -> account_response.JwtResponse:
    """
    ログイン
    """
    # emailを元にユーザーを取得
    user = db.query(models.User).filter(models.User.email == request.email).first()

    # ユーザーが存在するか
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="メールアドレスもしくはパスワードが間違っています"
        )

    # パスワードが正しいか
    if user.check_password(request.password) is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="メールアドレスもしくはパスワードが間違っています"
        )

    # トークンを返す
    access_token = authentication.create_access_token(user)
    refresh_token = authentication.create_refresh_token(user)
    return account_response.JwtResponse(
        access_token=access_token, refresh_token=refresh_token
    )


@router.post(
    "/v1/accounts/refresh-token",
    response_model=account_response.JwtResponse,
    summary=str(swagger_config.get_schemas()["accounts_refresh_token"]["summary"]),
    description=str(
        swagger_config.get_schemas()["accounts_refresh_token"]["description"]
    ),
    tags=list(swagger_config.get_schemas()["accounts_refresh_token"]["tags"]),
)
async def refresh_token(
    request: account_request.RefreshTokenRequest,
    db: Session = Depends(settings.get_db),
) -> account_response.JwtResponse:
    """
    トークンのリフレッシュ
    """

    user_id = authentication.user_id_from_refresh_token(request.refresh_token)
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="jwtの設定が正しくありません"
        )

    access_token = authentication.create_access_token(user)
    refresh_token = authentication.create_refresh_token(user)
    return account_response.JwtResponse(
        access_token=access_token, refresh_token=refresh_token
    )


@router.get(
    "/v1/accounts/me",
    response_model=account_response.AccountResponse,
    summary=str(swagger_config.get_schemas()["accounts_me"]["summary"]),
    description=str(swagger_config.get_schemas()["accounts_me"]["description"]),
    tags=list(swagger_config.get_schemas()["accounts_me"]["tags"]),
    dependencies=[
        Depends(authentication.get_user_and_decode_access_token),
    ],
)
async def me(
    auth_user=Depends(authentication.get_user_and_decode_access_token),
) -> account_response.AccountResponse:
    """
    自分の情報を取得
    """
    return account_response.AccountResponse.model_validate(auth_user)
