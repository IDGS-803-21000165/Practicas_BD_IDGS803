import os
from sqlalchemy import create_engine
import urllib


class Config(object):
    SECRET_KEY = 'Clave_Nueva'
    SESION_COOKIE_SECURE = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:monjiro19@127.0.0.1/pruebas'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
