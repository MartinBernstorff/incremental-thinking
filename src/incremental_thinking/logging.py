import logging


def my_handler(type, value, tb):
    logging.exception(
        "Uncaught exception: {}\n     Type: {}\n     Traceback: {}".format(
            str(value), str(type), str(tb)
        )
    )
    logging.exception(
        "If it's an addstr error, consider that the window might be overflowing"
    )
