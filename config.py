class Config(object):
    DEBUG = True


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False