from database.db import db


class Water(db.Model):
    __tablename__ = 'waters'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(10), nullable=False, default='off')

    def to_dict(self):
        return {"id": self.id, "status": self.status}
