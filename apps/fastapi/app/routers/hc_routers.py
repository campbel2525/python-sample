from fastapi import APIRouter, status
from fastapi.responses import HTMLResponse

from config import swagger_config

router = APIRouter()


@router.get(
    "/hc",
    response_class=HTMLResponse,
    summary=str(swagger_config.get_schemas()["hc"]["summary"]),
    description=str(swagger_config.get_schemas()["hc"]["description"]),
    tags=list(swagger_config.get_schemas()["hc"]["tags"]),
    responses={status.HTTP_200_OK: {"content": {"text/html": {"example": "Healthy."}}}},
)
async def send() -> HTMLResponse:
    """ヘルスチェック用のエンドポイント"""

    return HTMLResponse(content="Healthy.", status_code=status.HTTP_200_OK)
