import logging
from functools import wraps

from .Driver import Driver
from .Proxy import Proxy


def non_blocking(fun):
    @wraps(fun)
    def wrapped(*args, **kwargs):
        import threading
        def inner_fun():
            try:
                fun(*args, **kwargs)
            except Exception as e:
                logging.exception(e)

        th = threading.Thread(target=inner_fun)
        th.start()
    return wrapped
