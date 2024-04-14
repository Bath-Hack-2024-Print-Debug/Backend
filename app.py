from flask import Flask
from flask_cors import CORS


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
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

    import Preferences
    app.register_blueprint(Preferences.bp)

    import zoopla
    app.register_blueprint(zoopla.bp)

    return app