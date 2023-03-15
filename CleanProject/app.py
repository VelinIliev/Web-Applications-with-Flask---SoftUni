from decouple import config
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    f"postgresql://{config('DB_USER')}:{config('DB_PASSWORD')}" \
    f"@localhost:{config('DB_PORT')}/{config('DB_NAME')}"

db = SQLAlchemy(app)
from resources.auth import RegisterResource

api = Api(app)
migrate = Migrate(app, db)

api.add_resource(RegisterResource, '/register')

if __name__ == '__main__':
    app.run()
