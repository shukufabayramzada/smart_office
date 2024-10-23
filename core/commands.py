import click

from flask.cli import with_appcontext

from database.db import db
from models.light import Light
from models.water import Water


@click.command(name='add_sample_data')
@with_appcontext
def add_sample_data():
    # Add sample lights
    light1 = Light(id=1, status='false')
    light2 = Light(id=2, status='false')
    light3 = Light(id=3, status='false')
    light4 = Light(id=4, status='false')
    light5 = Light(id=5, status='false')
    light6 = Light(id=6, status='false')
    light7 = Light(id=7, status='false')
    light8 = Light(id=8, status='false')
    light9 = Light(id=9, status='false')
    light10 = Light(id=10, status='false')
    light11 = Light(id=11, status='false')
    light12 = Light(id=12, status='false')
    light13 = Light(id=13, status='false')
    light14 = Light(id=14, status='false')
    light15 = Light(id=15, status='false')
    light16 = Light(id=16, status='false')
    db.session.add_all([light1, light2, light3, light4, light5, light6, light7, light8,
                        light9, light10, light11, light12, light13, light14, light15, light16])
    db.session.commit()
    print("Light data added")

    # Add sample water systems
    water1 = Water(id=1, status='false')
    water2 = Water(id=2, status='false')
    db.session.add_all([water1, water2])
    db.session.commit()
    print("Water data added")

    print("Sample data added to the database")
