from flask import Flask
from strawberry.flask.views import AsyncGraphQLView
from api import schema

app = Flask(__name__)
app.add_url_rule(
    "/graphql",
    view_func=AsyncGraphQLView.as_view("graphql_view", schema=schema),
)
