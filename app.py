from flask import Flask
from config import Config
from models import db, bcrypt
from flask_jwt_extended import JWTManager
from routes import auth, movie

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)

app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(movie, url_prefix='/movie')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000)  # Change the port number
