from app.secure import *
import logging

class Config:
  SECRET_KEY = SECRET_KEY
  JSON_AS_ASCII = False
  JSON_SORT_KEYS = False
  DEBUG = True

  LOGGIONG_LEVEL = logging.DEBUG

  @staticmethod
  def init_app(app):
    pass


class DevelopmentConfig(Config):

  # SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
  SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI
  APPID=APPID
  APPSECRET=APPSECRET


class TestingConfig(Config):
  DEBUG = False
  SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI
  APPID=APPID
  APPSECRET=APPSECRET


class ProductionConfig(Config):
  SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:NetC@123@localhost:3306/partymember'
  APPID=APPID
  APPSECRET=APPSECRET

config = {'development': DevelopmentConfig,
          'testing': TestingConfig,
          'production': ProductionConfig,
          'default': DevelopmentConfig
          }
