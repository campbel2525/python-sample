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

    test = models.Test()
    test.name = "hogehoge"
    db.add(test)
    db.commit()


def test3():
    """
    DBから取得のサンプル
    """

    from app import models
    from config.settings import db

    result = db.query(models.Test).all()
    print(result)


def test4():
    """
    logのサンプル
    src/logs/python.logに出力されます
    """

    from app.utils.log import setup_logger

    logger = setup_logger(__name__)
    logger.info("This is a log message.")
    logger.error("This is an error message.")


if __name__ == "__main__":
    test1()
    test2()
    test3()
    test4()
