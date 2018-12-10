#encoding=utf8

class BaseConfig(object):
    pass


class TestConfig(BaseConfig):
    # 配置必须全大写，不然无法识别
    DATABASE = './instance/user.db'
    # SQLALCHEMY_DATABASE_URI = './instance/user.db'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///D:\\workspace\\helloPython\\advance\\awsjobs\\instance\\user.db'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1:3306/test'
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '123456'
    USERNAME = 'root'
    SECRET_KEY = 'a token test'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # mysqlhost = '127.0.0.1'
    MYSQLHOST = '127.0.0.1'
    MYSQLPORT = 3306
    MYSQLUSER = 'root'
    MYSQLPASSWORD = 'root'
    MYSQLDB = 'test'
    SESSION_TYPE = True

class DevConfig(BaseConfig):
    DB = 'xx.x.0x.1'


class ProConfig(BaseConfig):
    DB = 'xx.0x.0.1'