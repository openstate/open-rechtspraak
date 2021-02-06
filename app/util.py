import os


def get_env_variable(name, default=None) -> str:
    try:
        return os.environ.get(name, default=default)
    except KeyError:
        message = "Expected environment variable '{}' not set.".format(name)
        raise Exception(message)
