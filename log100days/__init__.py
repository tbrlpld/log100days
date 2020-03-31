import os

from quart import Quart
from dotenv import load_dotenv, find_dotenv

# To make .quartenv file work to set the Quart related environment variables.
# This is only for development purposes.
load_dotenv(find_dotenv(".quartenv"))


def get_setting_from_env(envvar_name: str, silent: bool = False) -> str:
    """
    Load an environment variable and return it's value.

    Parameters:
        envvar_name (String): Name of the environment variable to be loaded.
        silent (Bool): Boolean to control if a missing environment variable
            should pass silently or if an exceptions should be raised.
            Default: False.

    Returns:
        str: String value from the environment variable.

    Raises:
        KeyError: When a requested variable is not defined, this error is
            raised with a helpful message.
    """

    varval = os.getenv(envvar_name, default=None)
    if varval is None and not silent:
        raise KeyError(
            f"The environment variable {envvar_name} is missing."
            + " Be sure to configure it and try again.",
        )
    return varval


app = Quart(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY="dev",
    MARKDOWN_LOG_URL=get_setting_from_env("MARKDOWN_LOG_URL"),
    HOME_URL=get_setting_from_env("HOME_URL"),
)
# Override default config with settings from pyfile. This files needs to be
# placed in the "instance" folder. The "instance" folder can be directly in the
# repo (`./instance`) or in the environment in which Flask/Quart is installed
# (`.../venv/var/<appname>-instance/`).
app.config.from_pyfile("config.py", silent=True)

from log100days import routes
