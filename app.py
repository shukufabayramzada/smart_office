from flask import Flask
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from flask_migrate import Migrate

from api.light import light_bp
from api.water import water_bp
from core.commands import add_sample_data
from database.db import db

app = Flask(__name__)
CORS(app)


# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///smart_office.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)


# Swagger configuration
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
app.register_blueprint(light_bp)
app.register_blueprint(water_bp)

app.cli.add_command(add_sample_data)  # type: ignore


@app.route("/")
def index():
    return "Welcome to Smart Office!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
