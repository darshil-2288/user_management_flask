from flask import Flask
from bookmarks import bookmarks
from auth import auth
from database import db
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from config.swagger import template,swagger_config

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['JWT_SECRET_KEY']='JWT_SECRET_KEY'
SWAGGER={
    "title":"User API",
    "uiversion":3
}
JWTManager(app)

app.register_blueprint(auth)
app.register_blueprint(bookmarks)

Swagger(app,config=swagger_config,template=template)


db.app=app
db.init_app(app)
with app.app_context():
    db.create_all()

if __name__=="__main__":
	app.run(debug=True)
