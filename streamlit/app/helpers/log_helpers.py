import logging


def setup_logger(name="my_logger", log_file="logs/streamlit.log", level=logging.INFO):
    """To setup as many loggers as you want"""

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


# 使用用例
# from app.helpers import log_helpers
# logger = log_helpers.setup_logger(__name__)
# logger.info("This is a log message.")
# logger.error("This is an error message.")
