import click

from flask import Flask
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from flask_migrate import Migrate
from flask.cli import with_appcontext

from api.light import light_bp
from api.water import water_bp
from database.db import db
from models.light import Light
from models.water import Water


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


@click.command(name='add_sample_data')
@with_appcontext
def add_sample_data():
    # Add sample lights
    if not Light.query.first():
        light1 = Light(id=1, status='on')
        light2 = Light(id=2, status='on')
        light3 = Light(id=3, status='on')
        light4 = Light(id=4, status='on')
        light5 = Light(id=5, status='on')
        light6 = Light(id=6, status='on')
        light7 = Light(id=7, status='on')
        light8 = Light(id=8, status='on')
        light9 = Light(id=9, status='on')
        light10 = Light(id=10, status='on')
        light11 = Light(id=11, status='on')
        light12 = Light(id=12, status='on')
        light13 = Light(id=13, status='on')
        light14 = Light(id=14, status='on')
        light15 = Light(id=15, status='on')
        light16 = Light(id=16, status='on')
        db.session.add_all([light1, light2, light3, light4, light5, light6, light7, light8,
                            light9, light10, light11, light12, light13, light14, light15, light16])
        db.session.commit()

    # Add sample water systems
    if not Water.query.first():
        water1 = Water(id=1, status='on')
        water2 = Water(id=2, status='on')
        db.session.add_all([water1, water2])
        db.session.commit()

    print("Sample data added to the database.")


# Register the command with the Flask app
app.cli.add_command(add_sample_data)


# Routes
@app.route("/")
def index():
    return "Welcome to Smart Office!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
