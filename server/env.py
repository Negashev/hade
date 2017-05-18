from flask_env import MetaFlaskEnv

from server import app


class Configuration(metaclass=MetaFlaskEnv):
    pass


app.config.from_object(Configuration)