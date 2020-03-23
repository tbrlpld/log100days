from quart import Quart
from dotenv import load_dotenv, find_dotenv

# To make .quartenv file work to set the Quart related environment variables.
# This is only for development purposes.
load_dotenv(find_dotenv(".quartenv"))

app = Quart(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY="dev",
)
# Override default config with settings from pyfile.
app.config.from_pyfile("config.py", silent=True)

from log100days import routes
