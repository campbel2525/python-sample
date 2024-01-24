from app.routers import account_router, hc


def routing(app):
    app.include_router(hc.router)
    app.include_router(account_router.router)
