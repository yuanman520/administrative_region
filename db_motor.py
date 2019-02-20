#!/usr/bin/env python3

import motor

from config import MONGODB_HOST, MONGODB_PORT


class BaseMotor:
    def __init__(self):
        host_port = "{0}:{1}".format(MONGODB_HOST, MONGODB_PORT)
        uri = "mongodb://%s" % host_port
        self.client = motor.motor_tornado.MotorClient(uri)
