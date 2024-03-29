def debug():
    import debugpy

    debugpy.listen(("0.0.0.0", 9001))
    print("waiting ...")
    debugpy.wait_for_client()


# デバッグをする場合は下記のコメントアウトを外す
# debug()


def test1():
    x = 1
    y = 2
    z = x + y
    print(z)


def test2():
    """
    DBにinsertのサンプル
    """

    from app import models
    from config.settings import db

    test = models.User()
    test.name = "hogehoge"
    test.email = "test2@example.com"
    test.password = "password"
    db.add(test)
    db.commit()


def test3():
    """
    DBから取得のサンプル
    """

    from app import models
    from config.settings import db

    result = db.query(models.User).all()
    print(result)


def test4():
    """
    logのサンプル
    python/logs/python.logに出力されます
    """

    from app.helpers import log_helpers

    logger = log_helpers.setup_logger(__name__)
    logger.info("This is a log message.")
    logger.error("This is an error message.")


if __name__ == "__main__":
    test1()
    test2()
    test3()
    test4()
