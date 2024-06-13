from flask import Flask, session
from flask_session import Session
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from models import db, bcrypt
from flask_migrate import Migrate
from Routes import routes

app = Flask(__name__)

app.config.from_object(Config)
app.config['SESSION_TYPE'] = 'filesystem'

Session(app)
db.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)
CORS(app)

migrate = Migrate(app, db)

app.register_blueprint(routes)


@app.route('/')
def index():
    return "Flask app is running!"

if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()
    print("Running Flask application...")
    app.run(debug=True)

