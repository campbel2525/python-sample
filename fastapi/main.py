from fastapi import FastAPI

from config import debug_config, swagger_config
from routes import api_route

# デバッグの設定
debug_config.run_debug()

# appの定義
swagger_info = swagger_config.get_swagger_info()
app = FastAPI(**swagger_info)

# ルーティングの記述
api_route.routing(app)

# エラーハンドラー

# 必要なミドルウェアを設定する
