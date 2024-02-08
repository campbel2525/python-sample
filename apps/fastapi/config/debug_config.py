from config import settings


def run_debug():
    """
    debugpyはlocaldevv環境でのみinstallしているため
    import debugpy
    はこの関数内でやること
    """
    if settings.DEBUG:
        import debugpy

        debugpy.listen(("0.0.0.0", 9001))
