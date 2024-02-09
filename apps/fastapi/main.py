from fastapi import FastAPI

from config import debug_configs, swagger_configs
from routes import api_route

# デバッグの設定
debug_configs.run_debug()

# appの定義
swagger_info = swagger_configs.get_swagger_info()
app = FastAPI(**swagger_info)

# ルーティングの記述
api_route.routing(app)

# エラーハンドラー

# 必要なミドルウェアを設定する
