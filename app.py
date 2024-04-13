from flask import Flask
from flask_cors import CORS

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        JSON_ADD_STATUS=True,
        JSON_STATUS_FIELD_NAME="status"
    )
    CORS(app)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    import auth
    app.register_blueprint(auth.bp)

    import user
    app.register_blueprint(user.bp)

    import house
    app.register_blueprint(house.bp)

    return app