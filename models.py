from manage import db, app

class Shooting(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    place = db.Column(db.String(64), index=True, unique=True)
    count = db.Column(db.Integer, index=True)
    date = db.Column(db.DateTime, index=True)

    def __repr__(self):
        return '<Event %r>' % (self.place)

