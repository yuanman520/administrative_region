#!/usr/bin/env python3

import tornado.ioloop
import tornado.web

from config import BIND_IP, BIND_PORT
from handlers import QueryApiHandler


def make_app():
    return tornado.web.Application(handlers=[(r"/api", QueryApiHandler)], debug=True)


if __name__ == "__main__":
    app = make_app()
    app.listen(BIND_PORT, BIND_IP)
    tornado.ioloop.IOLoop.current().start()
