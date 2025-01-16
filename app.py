from flask import Flask
from models.db import db
from routes.api import blueprint as api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///api.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.register_blueprint(api)
with app.app_context():
    db.init_app(app)
    db.create_all()

if __name__ == '__main__':
    app.run('0.0.0.0',port=5000,debug=True)
