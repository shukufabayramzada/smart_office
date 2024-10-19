# models.py
from database.db import db


class Light(db.Model):
    __tablename__ = 'lights'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(10), nullable=False, default='off')

    def to_dict(self):
        return {"id": self.id, "status": self.status}

class WaterSystem(db.Model):
    __tablename__ = 'waters'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(10), nullable=False, default='off')

    def to_dict(self):
        return {"id": self.id, "status": self.status}
