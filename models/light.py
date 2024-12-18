from database.db import db


class Light(db.Model):
    __tablename__ = 'lights'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(10), nullable=False, default='false')

    def to_dict(self):
        return {"id": self.id, "status": self.status}
