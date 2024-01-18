class Config(object):
    ENV = "local"
    REDIS_URL = "redis://@redis:6379/0"


class DevConfig(Config):
    ENV = "dev"
    REDIS_URL = "rediss://red-cklv99jj89us738u33i0:c1vXNdmZhDpXxxOTrkEsaBM9m9Kgk67z@frankfurt-redis.render.com:6379"


class ProductionConfig(Config):
    ENV = "prod"
    REDIS_URL = 'https://eu2-outgoing-serval-31648.upstash.io'
