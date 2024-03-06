from flask import Flask
from flask_restful import Api


app = Flask(__name__)
api = Api(app)


# Routes
from assistant_api import AssistantApi
api.add_resource(AssistantApi, "/ask")


from assistant_feedback import AssistantFeedback
api.add_resource(AssistantFeedback, "/feedback")


if __name__ == "__main__":
    app.run(debug=True)
