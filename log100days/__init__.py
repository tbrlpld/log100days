from quart import Quart

app = Quart(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY="dev"
)
app.config.from_pyfile("config.py", silent=True)

from log100days import routes
