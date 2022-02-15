from sqlalchemy.sql import func
from app import db


class Top(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titel = db.Column(db.String(100), index=True, unique=False, nullable=False)
    eingereicht_von = db.Column(db.String(100), index=True, unique=False, nullable=False)
    eingereicht_am = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    frist = db.Column(db.Date, index=True, unique=False, nullable=True)
    beschreibung = db.Column(db.Text, nullable=True)
    abstimmungsfragen = db.Column(db.Text, nullable=True)
    archiviert = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return "<Top {} von {}>".format(self.titel, self.eingereicht_von)

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
