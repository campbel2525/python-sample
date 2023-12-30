def debug():
    import debugpy

    debugpy.listen(("0.0.0.0", 9001))
    print("waiting ...")
    debugpy.wait_for_client()


# デバッグをする場合は下記のコメントアウトを外す
# debug()


x = 1
y = 2

z = x + y

print(z)
