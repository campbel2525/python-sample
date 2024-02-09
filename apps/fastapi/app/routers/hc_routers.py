from fastapi import APIRouter, status
from fastapi.responses import HTMLResponse

from config import swagger_configs

router = APIRouter()


@router.get(
    "/hc",
    response_class=HTMLResponse,
    summary=str(swagger_configs.get_schemas()["hc"]["summary"]),
    description=str(swagger_configs.get_schemas()["hc"]["description"]),
    tags=list(swagger_configs.get_schemas()["hc"]["tags"]),
    responses={status.HTTP_200_OK: {"content": {"text/html": {"example": "Healthy."}}}},
)
async def send() -> HTMLResponse:
    """ヘルスチェック用のエンドポイント"""

    return HTMLResponse(content="Healthy.", status_code=status.HTTP_200_OK)
