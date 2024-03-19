from flask import Flask
from flask_restful import Api
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

api = Api(app)


# Routes
from assistant_api import AssistantApi
api.add_resource(AssistantApi, "/ask")


from assistant_feedback import AssistantFeedback
api.add_resource(AssistantFeedback, "/feedback")

from werkzeug.middleware.proxy_fix import ProxyFix

app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

if __name__ == "__main__":
    app.run(debug=True)
