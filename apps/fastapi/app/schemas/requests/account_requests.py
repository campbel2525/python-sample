from pydantic import BaseModel, EmailStr, Field


class SignUpRequest(BaseModel):
    name: str = Field(example="test1")
    email: EmailStr = Field(example="test1@example.com")
    password: str = Field(example="test1234")


class SignInRequest(BaseModel):
    email: EmailStr = Field(example="test1@example.com")
    password: str = Field(example="test1234")


class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(
        example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxOSwiZXhwIjoxNzA1OTUzNjcxLCJ0eXAiOiJyZWZyZXNoX3Rva2VuIn0.XU-gxVl2SdMMf_TYfV0Zu8VxkCzJT-Pt6v3hwxKMZrs"  # noqa
    )
