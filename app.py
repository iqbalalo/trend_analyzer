from flask import Flask
# from sync.sync import sync_blueprint
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.config.from_object('config.DevelopmentConfig')

# Register blueprints
# app.register_blueprint(sync_blueprint)

# Initiate db
# db.init_app(app)


# Create db tables
# @app.before_first_request
# def setup():
#     db.create_all()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)